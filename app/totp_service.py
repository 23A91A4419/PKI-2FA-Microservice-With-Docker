import base64
import pyotp
import time

def get_totp_generator(hex_seed: str) -> pyotp.TOTP:
    """
    Creates a TOTP generator from a hex seed.
    Converts hex seed to base32 as required by pyotp.
    """
    # Hex to bytes
    seed_bytes = bytes.fromhex(hex_seed)
    # Bytes to Base32
    seed_base32 = base64.b32encode(seed_bytes).decode('utf-8')
    # Create TOTP (SHA1, 30s, 6 digits are defaults for pyotp.TOTP)
    return pyotp.TOTP(seed_base32)

def generate_totp_code(hex_seed: str):
    """
    Generates the current TOTP code and remaining validity time.
    """
    totp = get_totp_generator(hex_seed)
    code = totp.now()
    # Calculate remaining time
    time_remaining = totp.interval - (time.time() % totp.interval)
    return code, int(time_remaining)

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verifies a TOTP code with a given validity window.
    valid_window=1 means ±1 period (30s).
    """
    totp = get_totp_generator(hex_seed)
    return totp.verify(code, valid_window=valid_window)
