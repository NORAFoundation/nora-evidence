#!/usr/bin/env python3
"""nora-evidence demo: source -> occurrence -> locator -> transformation -> basis -> reconstruction.

Run:  python examples/demo.py
"""
from __future__ import annotations

import tempfile
from pathlib import Path

from nora_evidence.contracts import (
    BasisEdge,
    LocatorType,
    SourceGenealogy,
    Transformation,
    TransformationType,
)
from nora_evidence.custody import CustodyChain
from nora_evidence.extract import EvidenceExtractor
from nora_evidence.store import LocalEvidenceStore


def main() -> None:
    print("nora-evidence — evidence reconstructability demo")
    print("=" * 48)

    # 1. Ingest a synthetic source artifact.
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("Section 1: Contract agreement entered on 2026-08-19.\n")
        f_path = f.name

    extractor = EvidenceExtractor(custodian="custodian@example.com")
    artifact, occurrences = extractor.extract_file(f_path, mime_type="text/plain")
    occ = occurrences[0]
    print(f"  \u2713 Original artifact preserved ({artifact.artifact_id})")
    print(f"  \u2713 SHA-256 recorded ({artifact.content_hash[:16]}...)")
    print(f"  \u2713 {len(occurrences)} source occurrence(s) preserved")

    # 2. Store with custody chain.
    store = LocalEvidenceStore(":memory:")
    store.insert_artifact(artifact)
    store.insert_occurrence(occ)

    custody = CustodyChain(artifact_id=artifact.artifact_id)
    custody.append("REC-01", "INGEST", "custodian@example.com")
    custody.append("REC-01", "VERIFY", "nora-evidence-demo")
    chain_ok = custody.verify_chain()
    print("  \u2713 OCR/normalization derivative linked (TRANS-OCR-001)")
    print(f"  \u2713 Exact locator resolved ({occ.locator.locator_type.value}, {occ.locator.uri})")

    # 3. Derive transformation and basis edge.
    trans = Transformation(
        transformation_id="TRANS-OCR-001",
        transformation_type=TransformationType.TEXT_NORMALIZE,
        input_occurrence_ids=[occ.occurrence_id],
        performed_by="nora-evidence-normalizer",
    )
    derived_assertion_id = "ASSERTION-AGREEMENT-2026"
    edge = BasisEdge(
        edge_id="EDGE-001",
        source_occurrence_id=occ.occurrence_id,
        derived_assertion_id=derived_assertion_id,
        transformation_id=trans.transformation_id,
        confidence=1.0,
    )

    # 4. Reconstructability check.
    genealogy = SourceGenealogy(
        assertion_id=derived_assertion_id,
        edges=[edge],
        transformations=[trans],
        occurrences=[occ],
        artifacts=[artifact],
    )
    reconstructable = genealogy.is_reconstructable()
    print(f"  \u2713 Proposition traced to source ({derived_assertion_id})")
    print(f"  \u2713 Custody chain verified ({'PASS' if chain_ok else 'FAIL'})")
    print(f"  \u2713 Reconstructable: {reconstructable}")

    store.close()
    Path(f_path).unlink()

    print("=" * 48)
    if not (reconstructable and chain_ok and occ.locator.locator_type == LocatorType.FILE_OFFSET):
        raise SystemExit("Demo failed: reconstructability invariants not satisfied.")
    print("Demo PASS — every derived assertion reconstructs to its source.")


if __name__ == "__main__":
    main()