# ADR-007: Audit Architecture

**Status**: Accepted  
**Date**: 2026-09-04  
**Decision**: SHA-256 hash-chain (primary) with optional Ethereum smart contract anchoring

## Context

VoiceGuard requires tamper-evident audit records for security decisions. The audit system must:
1. Provide tamper evidence (detect if records were modified)
2. Work without external blockchain infrastructure
3. Not store raw audio or sensitive personal data
4. Be verifiable independently
5. Not be part of the AI inference pipeline

## Decision

**Primary**: SHA-256 hash-chain stored in the database.  
**Optional**: Ethereum smart contract on local testnet (Hardhat/Ganache) for batch anchoring.

## Alternatives Considered

| Alternative | Reason Deferred |
|-------------|----------------|
| Full Ethereum (mainnet/testnet) | Requires gas fees, network connectivity, complex setup |
| Hyperledger Fabric | Heavy infrastructure; Docker required (unavailable) |
| IPFS + hash | Requires IPFS daemon; adds complexity |
| Simple database logging | No tamper evidence |

## Hash-Chain Design

```
Genesis → Event 1 → Event 2 → Event 3 → ...

Each event:
  data_hash = SHA256(canonical_json(event_data))
  chain_hash = SHA256(previous_chain_hash + data_hash + timestamp)
```

### Properties

- **Tamper-evident**: Modifying any event breaks the chain from that point forward.
- **Verifiable**: `POST /api/v1/audit/verify` recomputes and validates the entire chain.
- **No external dependency**: Runs entirely within the application database.
- **Append-only**: New events can only be added, not inserted or modified.

### What Goes On Chain

| Stored | NOT Stored |
|--------|-----------|
| Incident ID | Raw audio |
| Timestamp | Full transcript |
| Risk decision (score, level) | Personal information |
| Model version | Speaker embeddings |
| Verification result | Detailed analysis results |
| Evidence hash | |
| Action taken | |

## Optional Blockchain Anchoring

If Hardhat is available:
- Batch every N audit events
- Compute Merkle root of batch
- Submit to `AuditTrail.sol` smart contract
- Local Hardhat/Ganache network (no real ETH needed)

This adds blockchain-level tamper evidence on top of the hash-chain.

## Tradeoffs

- **Hash-chain in database**: If database is fully compromised, chain can be rebuilt from scratch by attacker. Blockchain anchoring mitigates this.
- **No external witness**: Hash-chain alone doesn't have an independent witness. Blockchain adds this.
- **Complexity vs. benefit**: For SIH prototype, hash-chain alone is sufficient and demonstrates the concept.

## Limitations

- Hash-chain provides tamper-evidence, not tamper-prevention.
- If the database and application are both compromised, the chain can be reconstructed by an attacker (unless blockchain-anchored).
- Blockchain anchoring requires Node.js tooling (Hardhat) which is available but adds setup time.
