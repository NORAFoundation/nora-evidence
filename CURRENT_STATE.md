# Current State — nora-evidence

**Status:** OSS EXTRACTION / RECONCILIATION IN PROGRESS
**Version:** 0.0.1

## Implemented Reference Slice

The minimum reference vertical slice is complete and verified:
`synthetic source -> occurrence -> locator -> transformation -> basis edge -> reconstructability check`

- `src/nora_evidence/contracts.py`: Dataclasses for `Artifact`, `SourceOccurrence`, `AcquisitionEvent`, `Transformation`, `Locator`, `BasisEdge`, and `SourceGenealogy`.
- `src/nora_evidence/custody.py`: Custody hash-chain appending and verification.
- `src/nora_evidence/store.py`: Offline-first SQLite + FTS5 evidence occurrence index.
- `src/nora_evidence/extract.py`: Multi-format evidence dispatcher generating exact Locators and SourceOccurrences.
- `src/nora_evidence/access.py`: Cleanroom `AcquisitionEnvelope` and `AccessPolicy` data classification.

## Contract Targets — Not Yet Implemented

The following symbols are described in documentation but are **not present** in the current source:

- `EvidenceStore` — canonical domain store backed by Postgres (not SQLite) with Matter/Occurrence schema and migrations
- `LocatorResolver` — external URL/DOI resolution adapter
- Object-store adapter for MinIO/S3 binary artifact persistence
## Verified

- `make test` / `pytest`: **7 passed in 0.11s**.
- Vertical-slice test path: `tests/test_vertical_slice.py`.
- Reconstructability and custody chain verification demonstrated end-to-end.

## Not Yet Established

- canonical feature parity;
- public extraction completeness;
- production deployment status;
- reconciliation of append-only SQLite triggers and cryptographic audit linking with canonical `matter-kernel`.
