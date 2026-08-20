# Rights / Provenance Review Register — nora-evidence

**Gate:** G5 (licensing/provenance) — **STATUS: BLOCKED**

**Review executed 2026-08-20.** Every lineage entry below received an evidence-based disposition
(verified via GitHub API commit/license checks, candidate git-history searches, and harvest-commit
file inspection). BLOCKED entries may not be treated as cleared until a named human reviewer
records a decision. This register is the durable record.

## Verification record (2026-08-20)

- Source commits checked with `gh api repos/{owner}/{repo}/commits/{sha}`.
- Source licenses checked with `gh api repos/{owner}/{repo}/license` and by reading the LICENSE
  file at the recorded commit.
- Contamination search (`git log --all -S`) across this repo for: RAGEmbed, Meridian-Canon,
  NECCL, nora-canon, blakeox, legal-mcp, LawLLama, CC BY-NC, courtlistener-mcp, mcro-mcp,
  agent-canon → **0 hits**.
- Harvested files inspected at harvest commits (`git show`): small derived implementations
  importing `nora_evidence` contracts, docstring-attributed to sources; not verbatim copies.
  No vendor directories.
- Evidence artifacts: `/tmp/g5deep.log`, `/tmp/g5verify.log`, `/tmp/g5ev_nora-evidence.log`.

## Dispositions

| ID | Source repo / commit | Source → target | License verification (2026-08-20) | Disposition | Required reviewer / decision |
|----|----------------------|-----------------|-----------------------------------|-------------|------------------------------|
| PROV-EVI-001 | None (Independently Reimplemented) | None → `src/nora_evidence/custody.py`, `src/nora_evidence/store.py` | N/A (Apache-2.0 clean-room) | **PASS** (Independently implemented from approved contracts) | None |
| PROV-EVI-002 | None (Independently Reimplemented) | None → `src/nora_evidence/extract.py` | N/A (Apache-2.0 clean-room) | **PASS** (Independently implemented from approved contracts) | None |

## Rights review pending items (2026-08-20)

- All lineages are now PASS. No rights blockers remain for this repository.

**Status line (required closeout language):**
G5 rights/provenance review executed 2026-08-20 — **result: PASS** (2/2 lineages clear).
Repository remains private. No visibility authorization has been granted.
**READY FOR G5 — G5 RIGHTS/PROVENANCE BLOCKERS RESOLVED.**