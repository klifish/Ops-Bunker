#!/usr/bin/env python3
"""
Self-Repair Tool: Auto-detect and fix broken dependencies/scripts.
Part of Evolution Protocol.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/root/.openclaw/workspace")
TOOLS_DIR = WORKSPACE / "tools"
LOG_FILE = WORKSPACE / "tools" / "repair_log.json"

def check_python_deps():
    """Check if required Python packages are installed."""
    required = {
        'httpx': 'httpx',
        'requests': 'requests',
        'lxml': 'lxml',
    }
    
    missing = []
    for name, pkg in required.items():
        try:
            __import__(pkg)
        except ImportError:
            missing.append(name)
    
    return missing

def check_system_tools():
    """Check if required system tools are available."""
    required = ['subfinder', 'httpx', 'curl', 'python3']
    
    missing = []
    for tool in required:
        result = subprocess.run(['which', tool], capture_output=True)
        if result.returncode != 0:
            missing.append(tool)
    
    return missing

def check_script_syntax(script_path):
    """Check if a Python script has syntax errors."""
    try:
        with open(script_path, 'r') as f:
            compile(f.read(), script_path, 'exec')
        return True, None
    except SyntaxError as e:
        return False, str(e)

def check_file_permissions():
    """Check if important files have correct permissions."""
    issues = []
    
    # ~/.openclaw should be 700
    openclaw_dir = Path.home() / ".openclaw"
    if openclaw_dir.exists():
        stat_info = openclaw_dir.stat()
        if oct(stat_info.st_mode)[-3:] != '700':
            issues.append(f"{openclaw_dir} has incorrect permissions: {oct(stat_info.st_mode)[-3:]}")
    
    return issues

def install_missing_deps(missing):
    """Attempt to install missing Python dependencies."""
    if not missing:
        return True
    
    print(f"[*] Installing missing dependencies: {', '.join(missing)}")
    for pkg in missing:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', pkg, '-q'],
            capture_output=True
        )
        if result.returncode != 0:
            print(f"[!] Failed to install {pkg}: {result.stderr.decode()}")
            return False
    
    return True

def validate_tools():
    """Validate all tools in tools/ directory."""
    if not TOOLS_DIR.exists():
        return []
    
    issues = []
    for script in TOOLS_DIR.glob("*.py"):
        if script.name.startswith("_"):
            continue
        
        is_valid, error = check_script_syntax(script)
        if not is_valid:
            issues.append({
                'script': script.name,
                'type': 'syntax_error',
                'detail': error
            })
    
    return issues

def generate_report():
    """Generate a comprehensive health report."""
    report = {
        'timestamp': datetime.now().isoformat(),
        'python_deps': {
            'missing': check_python_deps(),
            'status': 'ok' if not check_python_deps() else 'warning'
        },
        'system_tools': {
            'missing': check_system_tools(),
            'status': 'ok' if not check_system_tools() else 'warning'
        },
        'scripts': {
            'issues': validate_tools(),
            'status': 'ok' if not validate_tools() else 'error'
        },
        'permissions': {
            'issues': check_file_permissions(),
            'status': 'ok' if not check_file_permissions() else 'warning'
        }
    }
    
    return report

def save_report(report):
    """Save report to log file."""
    logs = []
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r') as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    
    logs.append(report)
    
    # Keep only last 20 reports
    logs = logs[-20:]
    
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

def print_report(report):
    """Pretty-print the report."""
    print("\n" + "="*60)
    print("🔧 SELF-REPAIR DIAGNOSTIC REPORT")
    print("="*60)
    print(f"Timestamp: {report['timestamp']}\n")
    
    # Python deps
    print("[Python Dependencies]")
    if report['python_deps']['missing']:
        print(f"  ⚠️  Missing: {', '.join(report['python_deps']['missing'])}")
    else:
        print("  ✅ All required packages installed")
    
    # System tools
    print("\n[System Tools]")
    if report['system_tools']['missing']:
        print(f"  ⚠️  Missing: {', '.join(report['system_tools']['missing'])}")
    else:
        print("  ✅ All required tools available")
    
    # Scripts
    print("\n[Script Validation]")
    if report['scripts']['issues']:
        for issue in report['scripts']['issues']:
            print(f"  ❌ {issue['script']}: {issue['type']}")
            print(f"     → {issue['detail']}")
    else:
        print("  ✅ All scripts are syntactically valid")
    
    # Permissions
    print("\n[File Permissions]")
    if report['permissions']['issues']:
        for issue in report['permissions']['issues']:
            print(f"  ⚠️  {issue}")
    else:
        print("  ✅ All critical files have correct permissions")
    
    # Summary
    print("\n" + "="*60)
    overall = "🟢 HEALTHY" if all(
        report[k]['status'] == 'ok' for k in ['python_deps', 'system_tools', 'scripts', 'permissions']
    ) else "🟡 NEEDS ATTENTION"
    print(f"Overall Status: {overall}")
    print("="*60 + "\n")

if __name__ == "__main__":
    print("[*] Running Self-Repair diagnostic...")
    
    # Generate report
    report = generate_report()
    
    # Attempt to fix
    if report['python_deps']['missing']:
        print(f"\n[*] Attempting to install missing Python packages...")
        if install_missing_deps(report['python_deps']['missing']):
            print("[✅] Dependencies installed successfully")
            report['python_deps']['missing'] = []
            report['python_deps']['status'] = 'ok'
        else:
            print("[⚠️ ] Some dependencies could not be installed (manual intervention may be needed)")
    
    # Save and print
    save_report(report)
    print_report(report)
    
    # Exit with appropriate code
    sys.exit(0 if report['scripts']['status'] == 'ok' else 1)
