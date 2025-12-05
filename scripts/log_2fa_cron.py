#!/usr/bin/env python3
# Cron script to log 2FA codes every minute

import os
from datetime import datetime, timezone

from totp_utils import generate_totp_code

SEED_PATH = "/data/seed.txt"


def main() -> None:
    """Read hex seed, generate TOTP code, print with UTC timestamp."""
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    if not os.path.exists(SEED_PATH):
        print(f"{now_utc} - Seed file not found at {SEED_PATH}")
        return

    with open(SEED_PATH, "r") as f:
        hex_seed = f.read().strip()

    if not hex_seed:
        print(f"{now_utc} - Seed file is empty")
        return

    try:
        code = generate_totp_code(hex_seed)
    except Exception as e:
        print(f"{now_utc} - Error generating TOTP code: {e}")
        return

    # Final required format:
    # "{timestamp} - 2FA Code: {code}"
    print(f"{now_utc} - 2FA Code: {code}")


if __name__ == "__main__":
    main()
