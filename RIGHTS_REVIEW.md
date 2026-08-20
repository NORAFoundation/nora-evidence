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
| PROV-EVI-001 | `NORAFoundation/meridian` @ `7059de20` | `src/meridian/custody.py`, `src/meridian/store.py` → `src/nora_evidence/custody.py`, `src/nora_evidence/store.py` | Commit **EXISTS**. LICENSE at `7059de20` = **MERIDIAN PROPRIETARY SOFTWARE LICENSE**. | **BLOCKED — LICENSE INCOMPATIBLE** (proprietary source; derived code may not be redistributed under Apache-2.0 without relicensing sign-off) | Named human reviewer with NORA Foundation relicensing authority |
| PROV-EVI-002 | `NORA-BITSY/Evidence_EXT` @ `a1b2c3d4` | `extractors/base.py` → `src/nora_evidence/extract.py` | Commit **DOES NOT EXIST** (GitHub 422 "No commit found"). Source repo has **no LICENSE file**. | **BLOCKED — SOURCE UNKNOWN** (recorded commit is a placeholder; original license unverifiable) | Named human reviewer to pin the real source commit + license, or authorize independent re-derivation |

## Rights review pending items (2026-08-20)

- Meridian-derived evidence implementation (PROV-EVI-001): proprietary source — relicensing or
  independent re-derivation required before any redistribution.
- Evidence_EXT placeholder provenance (PROV-EVI-002): recorded commit `a1b2c3d4` does not exist
  on GitHub; no license file in the source repo.

**Status line (required closeout language):**
G5 rights/provenance review executed 2026-08-20 — **result: BLOCKED** (0/2 lineages clear).
Repository remains private. No visibility authorization has been granted.
**NOT READY FOR PUBLICATION — G5 RIGHTS/PROVENANCE BLOCKERS REMAIN.**