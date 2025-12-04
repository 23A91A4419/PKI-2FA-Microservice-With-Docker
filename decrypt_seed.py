import base64
import os

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def load_private_key(path: str = "student_private.pem"):
    """Load RSA private key from PEM file."""
    with open(path, "rb") as f:
        pem_data = f.read()

    private_key = serialization.load_pem_private_key(
        pem_data,
        password=None,  # no password
    )
    return private_key


def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP.

    Args:
        encrypted_seed_b64: Base64-encoded ciphertext
        private_key: RSA private key object

    Returns:
        Decrypted hex seed (64-character string)
    """
    # 1. Base64 decode the encrypted seed string
    ciphertext = base64.b64decode(encrypted_seed_b64)

    # 2. RSA/OAEP decrypt with SHA-256
    plaintext_bytes = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # 3. Decode bytes to UTF-8 string
    seed_str = plaintext_bytes.decode("utf-8")

    # 4. Validate: must be 64-character hex string
    if len(seed_str) != 64:
        raise ValueError(f"Seed length must be 64, got {len(seed_str)}")

    allowed = "0123456789abcdef"
    if any(ch not in allowed for ch in seed_str):
        raise ValueError("Seed is not a valid lowercase hex string")

    # 5. Return hex seed
    return seed_str


def main():
    # Read encrypted seed from file
    with open("encrypted_seed.txt", "r") as f:
        encrypted_seed_b64 = f.read().strip()

    # Load private key
    private_key = load_private_key("student_private.pem")

    # Decrypt
    seed = decrypt_seed(encrypted_seed_b64, private_key)
    print("Decrypted seed:", seed)

    # Create data/ folder if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Save to data/seed.txt
    with open(os.path.join("data", "seed.txt"), "w") as f:
        f.write(seed)

    print("Saved decrypted seed to data/seed.txt")


if __name__ == "__main__":
    main()
