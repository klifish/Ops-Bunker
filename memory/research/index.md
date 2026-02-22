# Research: Blockchain Privacy & Cryptography

**Objective**: Align with Master L K's PhD research. Build a knowledge base to support brainstorming and potential Web3 security audits.

## 🔑 Key Concepts (To Be Expanded)

### 1. Zero-Knowledge Proofs (ZKP)
- **Definition**: Proving you know a secret without revealing the secret itself.
- **Use Cases**: Private transactions (Zcash, Monero), Scalability (zk-Rollups), Identity (zk-ID).
- **Attack Surface**: Circuit bugs, Trusted setup leaks, Weak fiat-shamir heuristic.

### 2. Multi-Party Computation (MPC)
- **Definition**: Multiple parties compute a function over their inputs while keeping inputs private.
- **Use Cases**: Threshold wallets (replacing Multisig), Privacy-preserving analytics.
- **Attack Surface**: Collusion, Maliciously secure vs Semi-honest models.

### 3. Homomorphic Encryption (HE)
- **Definition**: Computing on encrypted data.
- **Status**: Still computationally expensive, but the "Holy Grail".

## 📚 Reading List (Agents need to read too!)
- [ ] *The MoonMath Manual* (zk-SNARKs guide)
- [ ] *A Graduate Course in Applied Cryptography* (Boneh & Shoup)
- [ ] Immunefi Bug Reports (Real-world exploits)

## 🧠 Brainstorming: Privacy vs Auditability
- How to audit a smart contract that uses ZKPs if the logic is hidden in a circuit?
- Could we use `nuclei` to scan for common ZK circuit vulnerabilities (e.g., missing constraints)? (Potential tool idea!)
