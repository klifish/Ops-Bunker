import re
import sys
import argparse

def extract_intel(content):
    # Patterns for juicy things
    patterns = {
        'urls': r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*',
        'endpoints': r'["\'](/api/v\d+/[^"\']+|/v\d+/[^"\']+)["\']',
        'js_files': r'["\']([^"\']+\.js)["\']',
        'potential_keys': r'(api_key|access_token|secret)[-_]?\w*["\']?\s*[:=]\s*["\']?([a-zA-Z0-9-]{20,})["\']?'
    }

    results = {}
    for key, pattern in patterns.items():
        found = re.findall(pattern, content)
        if found:
            results[key] = list(set(found)) # Deduplicate
    
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extract_intel.py <filename>")
        sys.exit(1)
        
    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            intel = extract_intel(content)
            
            print(f"--- Intel Extracted from {filename} ---")
            for category, items in intel.items():
                print(f"\n[{category.upper()}]")
                for item in items:
                    print(f"  - {item}")
    except Exception as e:
        print(f"Error: {e}")
