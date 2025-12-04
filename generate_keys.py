from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_rsa_keypair(key_size: int = 4096):
    """
    Generate RSA key pair.

    Returns:
        (private_key, public_key)
    """
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # standard exponent
        key_size=key_size       # 4096 bits by default
    )

    # Get public key from private key
    public_key = private_key.public_key()

    return private_key, public_key


def save_keys():
    """Generate keys and save them as PEM files."""
    private_key, public_key = generate_rsa_keypair()

    # Save private key to student_private.pem
    with open("student_private.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),  # no password
            )
        )

    # Save public key to student_public.pem
    with open("student_public.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )


if __name__ == "__main__":
    save_keys()
