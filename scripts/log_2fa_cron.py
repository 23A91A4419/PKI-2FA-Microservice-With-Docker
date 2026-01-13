#!/usr/bin/env python3
import sys
import os
import datetime

# Add the parent directory to sys.path so we can import from app
# This is assuming the script is run from project root or handles paths correctly.
# In Docker, we set cwd to /app, but script is in /app/scripts.
# If we run as `python3 scripts/log_2fa_cron.py`, cwd is project root.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.totp_service import generate_totp_code
from app.config import settings

def main():
    try:
        if not os.path.exists(settings.SEED_FILE):
            print(f"Error: Seed file not found at {settings.SEED_FILE}", file=sys.stderr)
            sys.exit(1)
            
        with open(settings.SEED_FILE, "r") as f:
            hex_seed = f.read().strip()
            
        code, _ = generate_totp_code(hex_seed)
        
        # Get UTC timestamp
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        timestamp = now_utc.strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"{timestamp} - 2FA Code: {code}")
        
    except Exception as e:
        print(f"Error in cron job: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
