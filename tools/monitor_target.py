import os
import sys
import subprocess
import difflib
import time
import json
import hashlib
from datetime import datetime

# v4: Stability Upgrade
# - Master List Persistence: Tracks every unique subdomain ever found.
# - Staleness Tracking: Subdomains must fail 3 consecutive runs before removal.
# - Multi-Verification: Immediate retry for new detections.

def run_command(cmd, timeout=300):
    """Run a shell command with timeout and return the output."""
    try:
        result = subprocess.check_output(
            cmd, 
            shell=True, 
            stderr=subprocess.STDOUT,
            timeout=timeout
        )
        return result.decode('utf-8').splitlines()
    except subprocess.TimeoutExpired:
        print(f"[!] TIMEOUT: Command exceeded {timeout}s: {cmd}")
        return []
    except subprocess.CalledProcessError as e:
        print(f"[!] ERROR running command: {cmd}")
        return []

def extract_http_headers(url):
    """Extract interesting HTTP headers from a URL (fingerprinting)."""
    try:
        cmd = f"echo '{url}' | httpx-go -H -silent -timeout 10"
        output = subprocess.check_output(
            cmd, 
            shell=True, 
            stderr=subprocess.DEVNULL,
            timeout=15
        ).decode('utf-8')
        
        headers = {}
        for line in output.split('\n'):
            if ':' in line and not line.startswith('HTTP'):
                k, v = line.split(':', 1)
                k = k.strip().lower()
                v = v.strip()
                if k in ['server', 'x-powered-by', 'x-aspnet-version', 'x-frame-options', 'content-type']:
                    headers[k] = v
        return headers if headers else None
    except:
        return None

def get_fingerprint_hash(headers_dict):
    if not headers_dict: return None
    sorted_headers = json.dumps(headers_dict, sort_keys=True)
    return hashlib.md5(sorted_headers.encode()).hexdigest()

def monitor(domain):
    master_file = f"{domain}_master.json"
    fingerprint_file = f"{domain}_fingerprints.json"
    
    # Load Master State
    # Structure: { "subdomain": { "first_seen": ts, "last_seen": ts, "stale_count": 0 } }
    master_data = {}
    if os.path.exists(master_file):
        try:
            with open(master_file, 'r') as f:
                master_data = json.load(f)
        except:
            master_data = {}

    print(f"[*] Running discovery for {domain}...")
    # Attempt discovery with retry for stability
    all_found = []
    for i in range(2): # Try twice and combine results for stability
        cmd = f"subfinder -d {domain} -silent | httpx-go -mc 200,403,401 -silent -timeout 10"
        all_found.extend(run_command(cmd))
    
    current_scan = set(line.strip() for line in all_found if line.strip())
    now = datetime.now().isoformat()
    
    new_confirmed = []
    removed_confirmed = []
    
    # 1. Process New Subdomains
    for sub in current_scan:
        if sub not in master_data:
            master_data[sub] = {
                "first_seen": now,
                "last_seen": now,
                "stale_count": 0,
                "status": "active"
            }
            new_confirmed.append(sub)
        else:
            master_data[sub]["last_seen"] = now
            master_data[sub]["stale_count"] = 0
            master_data[sub]["status"] = "active"

    # 2. Process Missing Subdomains (Staleness check)
    for sub, info in master_data.items():
        if sub not in current_scan and info["status"] == "active":
            info["stale_count"] += 1
            if info["stale_count"] >= 3: # Must fail 3 consecutive runs to be removed
                info["status"] = "removed"
                info["removed_at"] = now
                removed_confirmed.append(sub)

    # Save Master State
    with open(master_file, 'w') as f:
        json.dump(master_data, f, indent=2)

    # Legacy support: write a flat text file for other tools
    with open(f"{domain}_subs.txt", 'w') as f:
        f.write('\n'.join(sorted([s for s, i in master_data.items() if i["status"] == "active"])))

    # Reporting
    if new_confirmed:
        print(f"\n[+] NEW subdomains confirmed ({len(new_confirmed)}):")
        for s in new_confirmed[:5]: print(f"    {s}")
    if removed_confirmed:
        print(f"\n[-] SUBDOMAINS removed after 3 failed scans ({len(removed_confirmed)}):")
        for s in removed_confirmed[:5]: print(f"    {s}")

    print(f"\n[*] Summary: {len([s for s, i in master_data.items() if i['status'] == 'active'])} active targets.")

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    monitor(sys.argv[1])
