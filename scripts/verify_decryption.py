import sys
import os

# Add parent dir
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import crypto_utils

def check():
    try:
        print("Loading private key...")
        priv_key = crypto_utils.load_private_key("student_private.pem")
        
        print("Loading encrypted seed...")
        with open("encrypted_seed.txt", "r") as f:
            enc_seed = f.read().strip()
            
        print("Decrypting...")
        seed = crypto_utils.decrypt_seed(enc_seed, priv_key)
        print(f"SUCCESS! Decrypted seed: {seed}")
        
    except Exception as e:
        print(f"FAILURE: {e}")

if __name__ == "__main__":
    check()
