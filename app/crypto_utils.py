import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

def load_private_key(path: str) -> rsa.RSAPrivateKey:
    with open(path, "rb") as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

def load_public_key(path: str) -> rsa.RSAPublicKey:
    with open(path, "rb") as key_file:
        return serialization.load_pem_public_key(
            key_file.read()
        )

def decrypt_seed(encrypted_seed_b64: str, private_key: rsa.RSAPrivateKey) -> str:
    """
    Decrypts the base64 encoded encrypted seed using RSA/OAEP-SHA256.
    Returns the decrypted hex string.
    """
    try:
        encrypted_bytes = base64.b64decode(encrypted_seed_b64)
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        decrypted_str = decrypted_bytes.decode('utf-8')
        
        # Validation
        if len(decrypted_str) != 64:
            raise ValueError("Decrypted seed length is not 64 characters")
        try:
            int(decrypted_str, 16) # Check if hex
        except ValueError:
             raise ValueError("Decrypted seed is not a valid hex string")
             
        return decrypted_str
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")

def sign_message(message: str, private_key: rsa.RSAPrivateKey) -> bytes:
    """
    Sign a message (commit hash) using RSA-PSS-SHA256.
    Message is expected to be the ascii string of the commit hash.
    """
    message_bytes = message.encode('utf-8')
    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def encrypt_with_public_key(data: bytes, public_key: rsa.RSAPublicKey) -> bytes:
    """
    Encrypt data using RSA/OAEP-SHA256.
    """
    encrypted = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted
