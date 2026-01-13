from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import os
from .config import settings
from . import crypto_utils, totp_service

app = FastAPI(title="PKI 2FA Microservice")

class EncryptedSeed(BaseModel):
    encrypted_seed: str

class VerificationRequest(BaseModel):
    code: str

@app.post("/decrypt-seed")
async def decrypt_seed_endpoint(payload: EncryptedSeed):
    """
    Decrypts the seed using student private key and stores it.
    """
    try:
        # Check if private key exists
        if not os.path.exists(settings.PRIVATE_KEY_PATH):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Private key not found"
            )

        # Load private key
        private_key = crypto_utils.load_private_key(settings.PRIVATE_KEY_PATH)

        # Decrypt seed
        decrypted_seed = crypto_utils.decrypt_seed(payload.encrypted_seed, private_key)

        # Ensure data directory exists
        os.makedirs(settings.DATA_DIR, exist_ok=True)

        # Save to persistent storage
        with open(settings.SEED_FILE, "w") as f:
            f.write(decrypted_seed)

        return {"status": "ok"}

    except ValueError as e:
        # Decryption error or validation error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Decryption failed"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/generate-2fa")
async def generate_2fa_endpoint():
    """
    Generates TOTP code from stored seed.
    """
    if not os.path.exists(settings.SEED_FILE):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Seed not decrypted yet"
        )
    
    try:
        with open(settings.SEED_FILE, "r") as f:
            hex_seed = f.read().strip()
            
        code, valid_for = totp_service.generate_totp_code(hex_seed)
        return {"code": code, "valid_for": valid_for}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/verify-2fa")
async def verify_2fa_endpoint(payload: VerificationRequest):
    """
    Verifies 2FA code.
    """
    if not os.path.exists(settings.SEED_FILE):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Seed not decrypted yet"
        )
        
    try:
        with open(settings.SEED_FILE, "r") as f:
            hex_seed = f.read().strip()
            
        is_valid = totp_service.verify_totp_code(hex_seed, payload.code)
        
        # Return {"valid": true/false}
        return {"valid": is_valid}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
