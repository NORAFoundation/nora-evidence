# Rights / Provenance Review Register — nora-evidence

**Gate:** G5 (licensing/provenance) — **STATUS: BLOCKED**

Formal external rights/provenance review is outstanding for every entry below.
This register is the durable record of each unresolved item. It is **not** a
resolution of any legal/rights question; no item below may be treated as cleared
until a named reviewer records a decision.

| ID | Source repo / commit / lineage | Source path(s) | Why review required | License / rights question | Evidence already collected | Required reviewer / decision | Remediation if rejected | Publication impact |
|----|-------------------------------|----------------|---------------------|---------------------------|---------------------------|------------------------------|-------------------------|--------------------|
| PROV-EVI-001 | `NORAFoundation/meridian` @ `7059de20` (internal NORA-authored) | `src/meridian/custody.py`, `src/meridian/store.py` → `src/nora_evidence/custody.py`, `src/nora_evidence/store.py` | Internal proprietary repo relicensed under Apache-2.0 for OSS distribution; relicensing requires explicit sign-off. | Was the internal relicensing decision authorized? Does any contributor hold competing rights? Original license: Proprietary. | SOURCE_PROVENANCE.yaml entry; secret_scan pass; privacy_scan pass; license_review pass (agent-level); `authorization_reference: INTERNAL_CLEANROOM_TRANSPLANT_PENDING_EXPLICIT_SIGN_OFF` | Named human reviewer with authority over NORA Foundation relicensing; explicit sign-off or rejection. | Remove/replace the migrated unit and re-derive from clean-room implementation; re-run all gates. | Blocks publication of nora-evidence (hard blocker per G5). |
| PROV-EVI-002 | `NORA-BITSY/Evidence_EXT` @ `a1b2c3d4` (placeholder commit — **provenance placeholder, commit not verified**) | `extractors/base.py` → `src/nora_evidence/extract.py` | Source commit `a1b2c3d4` is a placeholder, not a verified real commit; original license Unlicensed; repo lineage must be confirmed before relicensing. | Is `Evidence_EXT` NORA-authored? What is its actual commit and license? Placeholder provenance is not evidence. | SOURCE_PROVENANCE.yaml entry; secret/privacy/license scan pass (agent-level) on the *target* content. | Named reviewer to pin the real source commit + verify authorship/license; or confirm placeholder is acceptable. | Replace placeholder provenance with verified commit; or refactor/re-derive content; re-run gates. | Blocks publication of nora-evidence (hard blocker per G5). |

**Rights review pending items (inherited from evidence file):**
- `Evidence_EXT` history / placeholder provenance (PROV-EVI-002 above).
- Meridian-derived evidence implementation (PROV-EVI-001 above).

**Status line (required closeout language):**
Technical publication preparation complete. Formal rights/provenance review remains
outstanding. Repository remains private. No visibility authorization has been granted.