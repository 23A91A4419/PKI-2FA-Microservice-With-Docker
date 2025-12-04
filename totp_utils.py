import base64
import binascii
import hashlib

import pyotp


def _hex_to_base32(hex_seed: str) -> str:
    """
    Convert 64-character hex seed to base32 string.
    """
    # Basic validation
    if len(hex_seed) != 64:
        raise ValueError(f"hex_seed must be 64 chars, got {len(hex_seed)}")

    allowed = "0123456789abcdef"
    if any(ch not in allowed for ch in hex_seed):
        raise ValueError("hex_seed must be lowercase hex (0-9, a-f)")

    # 1. hex string -> bytes
    seed_bytes = binascii.unhexlify(hex_seed)

    # 2. bytes -> base32 string
    b32 = base64.b32encode(seed_bytes).decode("utf-8")

    return b32


def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current TOTP code from hex seed.

    Args:
        hex_seed: 64-character hex string

    Returns:
        6-digit TOTP code as string
    """
    # Convert hex seed to base32
    b32_seed = _hex_to_base32(hex_seed)

    # Create TOTP object (SHA-1, 30s, 6 digits are defaults)
    totp = pyotp.TOTP(
        b32_seed,
        interval=30,
        digits=6,
        digest=hashlib.sha1,
    )

    # Generate current TOTP code
    code = totp.now()

    return code


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify TOTP code with time window tolerance.

    Args:
        hex_seed: 64-character hex string
        code: 6-digit code to verify
        valid_window: number of periods before/after to accept (default 1)

    Returns:
        True if code is valid, False otherwise.
    """
    # Convert hex seed to base32
    b32_seed = _hex_to_base32(hex_seed)

    # Create TOTP object
    totp = pyotp.TOTP(
        b32_seed,
        interval=30,
        digits=6,
        digest=hashlib.sha1,
    )

    # Verify with time window tolerance
    return totp.verify(code, valid_window=valid_window)


# Small helper to test from command line:
if __name__ == "__main__":
    # Read your decrypted seed from data/seed.txt
    with open("data/seed.txt", "r") as f:
        hex_seed = f.read().strip()

    code = generate_totp_code(hex_seed)
    print("Current TOTP code:", code)

    # Quick self-check:
    print("Verify same code:", verify_totp_code(hex_seed, code))
