#!/usr/bin/env python3
"""
Decision Engine: Autonomous decision-making for security testing.
Analyzes targets, ranks risks, suggests priorities.
"""

import json
from datetime import datetime
from pathlib import Path

class SecurityTarget:
    def __init__(self, domain, url_list):
        self.domain = domain
        self.urls = url_list
        self.score = 0
        self.risk_factors = []
        self.recommendations = []
    
    def analyze(self):
        """Analyze target and compute risk score (0-100)."""
        score = 0
        
        # Factor 1: Domain indicators - higher priority for sensitive keywords
        priority_keywords = {
            'payment': 40,
            'billing': 40,
            'card': 35,
            'wallet': 35,
            'transaction': 30,
            'world': 35,         # Hyatt Gold Passport (member system) - upgraded
            'goldpassport': 40,  # Main loyalty system
            'member': 25,
            'support': 25,       # Support portal (downgraded - usually public/static)
            'api': 25,
            'admin': 30,
            'help': 15,          # Usually just FAQ (downgraded)
            'account': 20,
            'user': 15,
            'test': -15,        # Lower priority (likely test environment)
            'staging': -15,
            'uat': -15,
        }
        
        domain_lower = self.domain.lower()
        max_keyword_score = 0
        matched_keyword = None
        
        for keyword, points in priority_keywords.items():
            if keyword in domain_lower:
                if points > max_keyword_score:
                    max_keyword_score = points
                    matched_keyword = keyword
        
        score += max(0, max_keyword_score)  # No negative scores from keywords alone
        if matched_keyword:
            self.risk_factors.append(f"High-value target: {matched_keyword}")
        
        # Factor 2: URL count (more endpoints = larger attack surface)
        url_count = len(self.urls)
        if url_count > 100:
            score += 25
            self.risk_factors.append(f"Large attack surface ({url_count} URLs)")
        elif url_count > 50:
            score += 20
            self.risk_factors.append(f"Medium-large attack surface ({url_count} URLs)")
        elif url_count > 20:
            score += 10
            self.risk_factors.append(f"Medium attack surface ({url_count} URLs)")
        
        # Factor 3: Service type inference (more specific analysis)
        if 'support' in domain_lower:
            score += 20
            self.risk_factors.append("Support portal: IDOR, privilege escalation likely")
        elif 'payment' in domain_lower or 'billing' in domain_lower or 'card' in domain_lower:
            score += 30
            self.risk_factors.append("Financial target: high impact (fraud, data theft)")
        elif 'api' in domain_lower:
            score += 15
            self.risk_factors.append("API endpoint: auth bypass, data exposure risks")
        
        # Factor 4: Infrastructure hints (internal/staging = easier but less valuable)
        if 'internal' in domain_lower or 'int' in domain_lower:
            score -= 15
            self.risk_factors.append("Internal/staging (lower impact)")
        elif 'stg' in domain_lower or 'test' in domain_lower:
            score -= 15
            self.risk_factors.append("Test environment (lower impact)")
        elif 'prod' in domain_lower or 'production' in domain_lower or 'world' in domain_lower:
            score += 20
            self.risk_factors.append("Production environment (high impact)")
        
        self.score = max(0, min(score, 100))  # Cap between 0-100
        self.generate_recommendations()
        return self.score
    
    def generate_recommendations(self):
        """Generate testing recommendations based on score."""
        if self.score >= 80:
            self.recommendations = [
                "Prioritize authentication testing",
                "Test for IDOR and horizontal privilege escalation",
                "Check for business logic flaws",
                "Analyze payment/transaction flows if applicable"
            ]
        elif self.score >= 60:
            self.recommendations = [
                "Standard authentication testing",
                "IDOR checks on key resources",
                "Input validation and injection tests"
            ]
        else:
            self.recommendations = [
                "Basic reconnaissance first",
                "Assess information disclosure",
                "Check for common misconfigurations"
            ]
    
    def to_dict(self):
        return {
            'domain': self.domain,
            'risk_score': self.score,
            'risk_factors': self.risk_factors,
            'recommendations': self.recommendations,
            'url_count': len(self.urls)
        }

def rank_targets(targets_file='/root/.openclaw/workspace/hyatt.com_subs.txt'):
    """Analyze all targets and rank by risk."""
    
    if not Path(targets_file).exists():
        return []
    
    # Load URLs
    with open(targets_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    # Group by domain
    domains = {}
    for url in urls:
        # Extract domain from URL
        if '://' in url:
            domain = url.split('://')[1].split('/')[0]
        else:
            domain = url.split('/')[0]
        
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(url)
    
    # Analyze each domain
    targets = []
    for domain, url_list in domains.items():
        target = SecurityTarget(domain, url_list)
        target.analyze()
        targets.append(target)
    
    # Sort by risk score (highest first)
    targets.sort(key=lambda t: t.score, reverse=True)
    
    return targets

def generate_report(targets):
    """Generate a prioritized testing report."""
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_targets': len(targets),
        'highest_risk': targets[0].to_dict() if targets else None,
        'all_targets': [t.to_dict() for t in targets],
        'testing_plan': []
    }
    
    # Build testing plan (top 3 targets)
    for i, target in enumerate(targets[:3]):
        report['testing_plan'].append({
            'priority': i + 1,
            'domain': target.domain,
            'risk_score': target.score,
            'test_phases': target.recommendations
        })
    
    return report

if __name__ == "__main__":
    print("[*] Analyzing targets...\n")
    
    targets = rank_targets()
    
    if not targets:
        print("[!] No targets found.")
        exit(1)
    
    report = generate_report(targets)
    
    # Print report
    print("="*70)
    print("🎯 SECURITY TARGET PRIORITY REPORT")
    print("="*70)
    print(f"Total targets analyzed: {report['total_targets']}\n")
    
    print("📊 TOP 3 TARGETS (by risk):\n")
    for plan in report['testing_plan']:
        print(f"{plan['priority']}. {plan['domain']} (Risk Score: {plan['risk_score']}/100)")
        print(f"   Recommended phases:")
        for phase in plan['test_phases']:
            print(f"   - {phase}")
        print()
    
    print("="*70)
    print(f"\nFull report saved to: hyatt_priority_analysis.json")
    
    # Save report
    with open('/root/.openclaw/workspace/hyatt_priority_analysis.json', 'w') as f:
        json.dump(report, f, indent=2)
