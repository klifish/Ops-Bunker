import os
import time
import sys
import json

# Configuration
HONEYPOT_FILE = "secret_keys.txt"
STATE_FILE = "tools/canary_state.json"

def create_honeypot():
    if not os.path.exists(HONEYPOT_FILE):
        with open(HONEYPOT_FILE, 'w') as f:
            f.write("AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE\n")
            f.write("AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY\n")
            f.write("# DO NOT COMMIT THIS FILE\n")
        # Set initial state
        update_state(os.path.getatime(HONEYPOT_FILE))
        print(f"[*] Honeypot created at {HONEYPOT_FILE}")

def update_state(atime):
    with open(STATE_FILE, 'w') as f:
        json.dump({"last_atime": atime}, f)

def check_canary():
    if not os.path.exists(HONEYPOT_FILE):
        create_honeypot()
        return

    if not os.path.exists(STATE_FILE):
        update_state(os.path.getatime(HONEYPOT_FILE))
        return

    with open(STATE_FILE, 'r') as f:
        state = json.load(f)
    
    current_atime = os.path.getatime(HONEYPOT_FILE)
    
    # If file accessed (atime changed)
    if current_atime > state["last_atime"]:
        print(f"[!] CANARY TRIGGERED! File accessed at {time.ctime(current_atime)}")
        # In a real scenario, this would trigger the LOCKDOWN protocol
        # For now, we just log it.
        update_state(current_atime)
    else:
        print("[-] Canary safe.")

if __name__ == "__main__":
    check_canary()
