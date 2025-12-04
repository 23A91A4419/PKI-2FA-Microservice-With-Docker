import json
import requests

def request_seed(student_id: str, github_repo_url: str, api_url: str):
    """
    Request encrypted seed from instructor API
    """

    # Step 1: Read student public key
    with open("student_public.pem", "r") as f:
        public_key = f.read()

    # Step 2: Prepare payload
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key
    }

    # Step 3: Send POST request
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)

    # Step 4: Parse JSON response
    if response.status_code != 200:
        print("Error:", response.text)
        return

    data = response.json()
    encrypted_seed = data.get("encrypted_seed")

    # Step 5: Save encrypted seed to file
    with open("encrypted_seed.txt", "w") as f:
        f.write(encrypted_seed)

    print("Encrypted seed saved to encrypted_seed.txt")



if __name__ == "__main__":
    request_seed(
        student_id="23A91A4419",   
        github_repo_url="https://github.com/23A91A4419/PKI-2FA-Microservice-With-Docker",
        api_url="https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"
    )
