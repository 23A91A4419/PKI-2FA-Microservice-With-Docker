import base64

try:
    with open("encrypted_seed.txt", "r") as f:
        content = f.read().strip()
    
    print(f"Length: {len(content)}")
    print(f"Content: {content}")
    
    # Try decode
    decoded = base64.b64decode(content)
    print(f"Decoded length: {len(decoded)}")
    print(f"Decoded hex: {decoded.hex()}")
except Exception as e:
    print(f"Error: {e}")
