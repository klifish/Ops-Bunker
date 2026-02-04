import os
import sys
import subprocess
import difflib
import time

def run_command(cmd):
    """Run a shell command and return the output."""
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return result.decode('utf-8').splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}\n{e.output.decode('utf-8')}")
        return []

def monitor(domain):
    filename = f"{domain}_subs.txt"
    old_subs = []
    
    # Load old state
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            old_subs = sorted([line.strip() for line in f if line.strip()])
    
    print(f"[*] Running subfinder on {domain}...")
    # Run subfinder (silent mode) -> httpx (filter garbage)
    # Evolution: Added httpx filtering to ignore 301/404 noise immediately
    cmd = f"subfinder -d {domain} -silent | httpx -mc 200,403,401 -silent"
    new_subs = run_command(cmd)
    new_subs = sorted(list(set(new_subs))) # Dedup and sort
    
    # Save new state immediately
    with open(filename, 'w') as f:
        f.write('\n'.join(new_subs))
        
    # Compare
    diff = list(difflib.unified_diff(old_subs, new_subs, fromfile='old', tofile='new', lineterm=''))
    
    new_entries = [line[1:] for line in diff if line.startswith('+') and not line.startswith('+++')]
    
    if new_entries:
        print(f"\n[!] ALERT: {len(new_entries)} new subdomains found for {domain}!")
        for sub in new_entries:
            print(f"  + {sub}")
    else:
        print(f"\n[-] No changes detected for {domain}. ({len(new_subs)} subdomains total)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 monitor_target.py <domain>")
        sys.exit(1)
        
    target_domain = sys.argv[1]
    monitor(target_domain)
