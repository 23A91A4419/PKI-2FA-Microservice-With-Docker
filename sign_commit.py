import base64
import subprocess

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


# ---------- Helper: load keys ----------

def load_student_private_key(path: str = "student_private.pem"):
    """Load RSA private key from PEM file."""
    with open(path, "rb") as f:
        key_data = f.read()
    private_key = serialization.load_pem_private_key(
        key_data,
        password=None,
    )
    return private_key


def load_instructor_public_key(path: str = "instructor_public.pem"):
    """Load RSA public key from PEM file."""
    with open(path, "rb") as f:
        key_data = f.read()
    public_key = serialization.load_pem_public_key(key_data)
    return public_key


# ---------- Step 1: sign_message ----------

def sign_message(message: str, private_key) -> bytes:
    """
    Sign a message using RSA-PSS with SHA-256.

    Implementation:
    1. Encode commit hash as ASCII/UTF-8 bytes
    2. Sign using RSA-PSS:
       - Padding: PSS
       - MGF1: SHA-256
       - Hash: SHA-256
       - Salt length: MAX_LENGTH
    """
    # 1. Convert string -> bytes
    msg_bytes = message.encode("utf-8")  # ASCII-safe

    # 2. Sign with RSA-PSS-SHA256
    signature = private_key.sign(
        msg_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )

    return signature


# ---------- Step 2: encrypt_with_public_key ----------

def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    """
    Encrypt data using RSA/OAEP with public key.

    Implementation:
    - Padding: OAEP
    - MGF1: SHA-256
    - Hash: SHA-256
    - Label: None
    """
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return ciphertext


# ---------- Step 3: get current commit hash ----------

def get_current_commit_hash() -> str:
    """
    Get latest commit hash (40-character hex) using Git.
    """
    result = subprocess.run(
        ["git", "log", "-1", "--format=%H"],
        capture_output=True,
        text=True,
        check=True,
    )
    commit_hash = result.stdout.strip()
    # Should already be 40 chars
    return commit_hash


# ---------- Step 4: glue everything together ----------

def generate_commit_proof():
    # 1. Get commit hash
    commit_hash = get_current_commit_hash()

    # 2. Load keys
    student_private = load_student_private_key("student_private.pem")
    instructor_public = load_instructor_public_key("instructor_public.pem")

    # 3. Sign commit hash with student private key
    signature = sign_message(commit_hash, student_private)

    # 4. Encrypt signature with instructor public key (OAEP-SHA256)
    encrypted_sig = encrypt_with_public_key(signature, instructor_public)

    # 5. Base64-encode encrypted signature for submission
    encrypted_sig_b64 = base64.b64encode(encrypted_sig).decode("ascii")

    # 6. Print results exactly as needed
    print("Commit Hash:")
    print(commit_hash)
    print()
    print("Encrypted Signature (Base64):")
    print(encrypted_sig_b64)


if __name__ == "__main__":
    generate_commit_proof()
