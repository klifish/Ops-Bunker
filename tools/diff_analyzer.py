import requests
import json
from datetime import datetime

nodes = ["EU-DE-1", "BR-E-1", "US-C-1", "AU-S-1", "IN-W-1"]
base_url = "https://c65244-{}.beyondtrustcloud.com/"
results = {}

print(f"[*] Starting differential analysis for Hyatt BeyondTrust nodes...")

for node in nodes:
    url = base_url.format(node)
    try:
        # Check root
        r1 = requests.get(url, timeout=10)
        # Check for a common sensitive but often restricted path
        r2 = requests.get(url + "login", timeout=10)
        
        results[node] = {
            "root_status": r1.status_code,
            "root_length": len(r1.text),
            "login_status": r2.status_code,
            "server": r1.headers.get("Server"),
            "x-trace-id": r1.headers.get("X-Trace-Id"),
            "powered_by": r1.headers.get("X-Powered-By")
        }
        print(f"[+] Node {node}: Status {r1.status_code}, Login {r2.status_code}")
    except Exception as e:
        print(f"[-] Node {node} failed: {e}")

with open("hyatt_node_diff_analysis.json", "w") as f:
    json.dump(results, f, indent=4)

print(f"[*] Analysis complete. Saved to hyatt_node_diff_analysis.json")
