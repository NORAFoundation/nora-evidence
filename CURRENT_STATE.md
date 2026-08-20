# Current State — nora-evidence

**Status:** IMPLEMENTED (Minimum Vertical Slice Verified)  
**Version:** 0.0.1  

## Implemented Vertical Slice

The required minimum vertical slice is complete and verified:
`synthetic source -> occurrence -> locator -> transformation -> basis edge -> reconstructability check`

- `src/nora_evidence/contracts.py`: Dataclasses for `Artifact`, `SourceOccurrence`, `AcquisitionEvent`, `Transformation`, `Locator`, `BasisEdge`, and `SourceGenealogy`.
- `src/nora_evidence/custody.py`: Custody hash-chain appending and verification.
- `src/nora_evidence/store.py`: Offline-first SQLite + FTS5 evidence occurrence index.
- `src/nora_evidence/extract.py`: Multi-format evidence dispatcher generating exact Locators and SourceOccurrences.
- `src/nora_evidence/access.py`: Cleanroom `AcquisitionEnvelope` and `AccessPolicy` data classification.

## Verification Evidence

- `make test` / `pytest`: **6 passed in 0.12s**.
- Full end-to-end reconstructability and custody chain verification demonstrated in `tests/test_vertical_slice.py`.
