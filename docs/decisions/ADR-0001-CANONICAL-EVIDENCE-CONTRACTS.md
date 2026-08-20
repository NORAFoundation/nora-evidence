# ADR-0001: Canonical Evidence Contracts and Reconstructability Invariants

- **Status:** Accepted
- **Date:** 2026-08-19
- **Deciders:** NORA Foundation Engineering Team

## Context

A core invariant of the NORA evidence substrate is that derived assertions must remain reconstructable to exact source occurrences and raw artifacts (`policies/PRIVACY_FIREWALL.md`, `AGENTS.md`).

## Decision

We adopt strict, immutable data contracts for:
1. `Artifact` — Raw acquired blob with cryptographic hash and `AcquisitionEvent`.
2. `SourceOccurrence` — Precise instance bounded by an exact `Locator` (offset, page span, text span, timestamp).
3. `Transformation` — Provenance-bearing operation (`ocr_extract`, `audio_transcribe`, etc.) applied to input occurrences.
4. `BasisEdge` — Explicit connection between source occurrences, transformations, and derived assertions.
5. `SourceGenealogy` — Full reconstructability graph asserting zero orphan assertions.

## Consequences

- All derived assertions must carry a valid `SourceGenealogy` graph.
- `is_reconstructable()` returns `False` if any basis edge references missing occurrences or transformations.
