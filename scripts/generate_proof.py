import sys
import os
import base64
import argparse
import subprocess

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import crypto_utils

def generate_proof(private_key_path: str, instructor_key_path: str):
    if not os.path.exists(private_key_path):
        print(f"Error: Student private key not found at {private_key_path}")
        return
    if not os.path.exists(instructor_key_path):
        print(f"Error: Instructor public key not found at {instructor_key_path}")
        return

    # 1. Get Commit Hash
    try:
        commit_hash = subprocess.check_output(
            ["git", "log", "-1", "--format=%H"], 
            stderr=subprocess.STDOUT
        ).decode("utf-8").strip()
        print(f"Commit Hash: {commit_hash}")
    except subprocess.CalledProcessError as e:
        print("Error getting git commit hash. Are you in a git repo?")
        return

    # 2. Load Keys
    student_private_key = crypto_utils.load_private_key(private_key_path)
    instructor_public_key = crypto_utils.load_public_key(instructor_key_path)

    # 3. Sign Commit Hash
    signature = crypto_utils.sign_message(commit_hash, student_private_key)

    # 4. Encrypt Signature
    encrypted_signature = crypto_utils.encrypt_with_public_key(signature, instructor_public_key)
    
    # 5. Base64 Encode
    encrypted_signature_b64 = base64.b64encode(encrypted_signature).decode("utf-8")
    
    # Write to file directly to avoid shell encoding issues
    proof_content = f"""Commit Hash: {commit_hash}
Encrypted Signature (Single Line):
{encrypted_signature_b64}"""
    
    with open("proof_final.txt", "w", encoding="utf-8") as f:
        f.write(proof_content)

    print("\n--- SUBMISSION PROOF GENERATED (proof_final.txt) ---")
    print(f"Commit Hash: {commit_hash}")
    print("Encrypted Signature (Single Line):")
    print(encrypted_signature_b64)
    print("------------------------")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate submission proof")
    parser.add_argument("--private-key", default="student_private.pem", help="Path to student private key")
    parser.add_argument("--instructor-key", default="instructor_public.pem", help="Path to instructor public key")
    
    args = parser.parse_args()
    generate_proof(args.private_key, args.instructor_key)
