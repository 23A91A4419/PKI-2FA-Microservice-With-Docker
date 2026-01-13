import requests
import time
import os
import sys

BASE_URL = "http://localhost:8080"
SEED_FILE = "encrypted_seed.txt"

def wait_for_service():
    print("Waiting for service to start...")
    for i in range(30):
        try:
            requests.get(f"{BASE_URL}/docs")
            print("Service is up!")
            return True
        except:
            time.sleep(1)
            print(".", end="", flush=True)
    print("\nService failed to start.")
    return False

def test_endpoints():
    # 1. Decrypt Seed
    if not os.path.exists(SEED_FILE):
        print(f"Error: {SEED_FILE} not found.")
        return False
        
    with open(SEED_FILE, 'r') as f:
        encrypted_seed = f.read().strip()
    
    print("\n1. Testing /decrypt-seed...")
    try:
        resp = requests.post(f"{BASE_URL}/decrypt-seed", json={"encrypted_seed": encrypted_seed})
        print(f"Status: {resp.status_code}, Response: {resp.json()}")
        if resp.status_code != 200:
            return False
    except Exception as e:
        print(f"Failed: {e}")
        return False

    # 2. Generate 2FA
    print("\n2. Testing /generate-2fa...")
    try:
        resp = requests.get(f"{BASE_URL}/generate-2fa")
        print(f"Status: {resp.status_code}, Response: {resp.json()}")
        if resp.status_code != 200:
            return False
        data = resp.json()
        code = data.get("code")
    except Exception as e:
        print(f"Failed: {e}")
        return False

    # 3. Verify 2FA
    print(f"\n3. Testing /verify-2fa with code {code}...")
    try:
        resp = requests.post(f"{BASE_URL}/verify-2fa", json={"code": code})
        print(f"Status: {resp.status_code}, Response: {resp.json()}")
        if resp.status_code != 200 or not resp.json().get("valid"):
            print("Verification failed!")
            return False
    except Exception as e:
        print(f"Failed: {e}")
        return False
        
    print("\nAll endpoints verified successfully!")
    return True

if __name__ == "__main__":
    if wait_for_service():
        if not test_endpoints():
            sys.exit(1)
    else:
        sys.exit(1)
