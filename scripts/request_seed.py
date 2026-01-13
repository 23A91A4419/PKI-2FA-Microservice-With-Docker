import requests
import json
import os
import argparse

def request_seed(student_id: str, github_repo_url: str, public_key_path: str):
    api_url = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"
    
    if not os.path.exists(public_key_path):
        print(f"Error: Public key file not found at {public_key_path}")
        return

    with open(public_key_path, "r") as f:
        public_key_pem = f.read()

    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key_pem
    }

    print(f"Requesting seed for {student_id} from {github_repo_url}...")
    
    try:
        response = requests.post(
            api_url, 
            json=payload, 
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        if "encrypted_seed" in data:
            encrypted_seed = data["encrypted_seed"]
            with open("encrypted_seed.txt", "w") as f:
                f.write(encrypted_seed)
            print("Success! Encrypted seed saved to 'encrypted_seed.txt'.")
            print("Note: Do NOT commit this file to Git.")
        else:
            print("Error: 'encrypted_seed' not found in response.")
            print("Response:", data)
            
    except requests.exceptions.RequestException as e:
        print(f"API Request failed: {e}")
        if hasattr(e, 'response') and e.response is not None: # type: ignore
            print("Response content:", e.response.text) # type: ignore

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Request encrypted seed from instructor API")
    parser.add_argument("student_id", help="Your Student ID")
    parser.add_argument("repo_url", help="Your GitHub Repository URL")
    parser.add_argument("--key", default="student_public.pem", help="Path to student public key")
    
    args = parser.parse_args()
    request_seed(args.student_id, args.repo_url, args.key)
