import os

class Settings:
    # Use absolute paths or defaults relative to execution context
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Data directory for persistent storage
    DATA_DIR = os.getenv("DATA_DIR", os.path.join(BASE_DIR, "data"))
    
    # Path to the decrypted seed file
    SEED_FILE = os.path.join(DATA_DIR, "seed.txt")
    
    # Path to student private key
    # In Docker, we might mount this or copy it. Default to root dir.
    PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH", os.path.join(BASE_DIR, "student_private.pem"))

settings = Settings()
