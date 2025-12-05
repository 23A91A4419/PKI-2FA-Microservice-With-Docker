import os
import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from decrypt_seed import load_private_key, decrypt_seed
from totp_utils import generate_totp_code, verify_totp_code

app = FastAPI()

SEED_PATH = os.path.join("data", "seed.txt")


# ---------- Request Models ----------

class DecryptSeedRequest(BaseModel):
    encrypted_seed: str


class VerifyCodeRequest(BaseModel):
    code: str


# ---------- Helper Functions ----------

def read_hex_seed() -> str:
    """Read hex seed from data/seed.txt."""
    if not os.path.exists(SEED_PATH):
        raise FileNotFoundError("Seed not decrypted yet")

    with open(SEED_PATH, "r") as f:
        hex_seed = f.read().strip()

    if len(hex_seed) != 64:
        raise ValueError("Seed is not 64-character hex")

    return hex_seed


def save_hex_seed(hex_seed: str) -> None:
    """Save hex seed to data/seed.txt."""
    os.makedirs(os.path.dirname(SEED_PATH), exist_ok=True)
    with open(SEED_PATH, "w") as f:
        f.write(hex_seed)


# ---------- Endpoint 1: POST /decrypt-seed ----------

@app.post("/decrypt-seed")
def api_decrypt_seed(payload: DecryptSeedRequest):
    """
    Decrypt encrypted_seed and save hex seed to data/seed.txt.
    """
    try:
        # Load private key
        private_key = load_private_key("student_private.pem")

        # Decrypt (decrypt_seed already does Base64 decode + RSA/OAEP/SHA256)
        hex_seed = decrypt_seed(payload.encrypted_seed, private_key)

        # Validate 64-char hex (decrypt_seed already checks, but double-check)
        if len(hex_seed) != 64:
            raise ValueError("Decrypted seed is not 64 characters")

        save_hex_seed(hex_seed)

        return {"status": "ok"}

    except Exception as e:
        # In production you’d log e
        raise HTTPException(status_code=500, detail="Decryption failed")


# ---------- Endpoint 2: GET /generate-2fa ----------

@app.get("/generate-2fa")
def api_generate_2fa():
    """
    Generate current TOTP code and return how many seconds it is valid for.
    """
    try:
        # 1. Check if seed exists & read it
        hex_seed = read_hex_seed()

        # 2. Generate TOTP code
        code = generate_totp_code(hex_seed)

        # 3. Calculate remaining seconds in current 30s window
        now = int(time.time())
        remaining = 30 - (now % 30)

        return {
            "code": code,
            "valid_for": remaining,
        }

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to generate 2FA code")


# ---------- Endpoint 3: POST /verify-2fa ----------

@app.post("/verify-2fa")
def api_verify_2fa(payload: VerifyCodeRequest):
    """
    Verify submitted TOTP code.
    """
    # 1. Validate code present
    code = payload.code
    if not code:
        raise HTTPException(status_code=400, detail="Missing code")

    try:
        # 2. Make sure seed exists & read it
        hex_seed = read_hex_seed()

        # 3. Verify TOTP with ±1 period tolerance
        is_valid = verify_totp_code(hex_seed, code, valid_window=1)

        return {"valid": is_valid}

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    except Exception:
        raise HTTPException(status_code=500, detail="Verification failed")
