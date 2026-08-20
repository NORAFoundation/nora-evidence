import tempfile
from pathlib import Path
import pytest
from nora_evidence.contracts import (
    BasisEdge,
    LocatorType,
    SourceGenealogy,
    Transformation,
    TransformationType
)
from nora_evidence.custody import CustodyChain
from nora_evidence.extract import EvidenceExtractor
from nora_evidence.store import LocalEvidenceStore

def test_nora_evidence_minimum_vertical_slice():
    """
    Minimum Vertical Slice:
    synthetic source -> register source occurrence -> create exact locator
    -> derive one transformation -> create basis edge -> reconstructability check
    """
    # 1. Ingest synthetic source file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("Section 1: Contract agreement entered on 2026-08-19.\n")
        f_path = f.name
        
    extractor = EvidenceExtractor(custodian="custodian@example.com")
    artifact, occurrences = extractor.extract_file(f_path, mime_type="text/plain")
    assert len(occurrences) == 1
    occ = occurrences[0]
    
    # 2. Store in local evidence store + custody chain
    store = LocalEvidenceStore(":memory:")
    store.insert_artifact(artifact)
    store.insert_occurrence(occ)
    
    custody = CustodyChain(artifact_id=artifact.artifact_id)
    custody.append("REC-01", "INGEST", "custodian@example.com")
    assert custody.verify_chain() is True

    # 3. Derive transformation and basis edge
    trans = Transformation(
        transformation_id="TRANS-OCR-001",
        transformation_type=TransformationType.TEXT_NORMALIZE,
        input_occurrence_ids=[occ.occurrence_id],
        performed_by="nora-evidence-normalizer"
    )

    derived_assertion_id = "ASSERTION-AGREEMENT-2026"
    edge = BasisEdge(
        edge_id="EDGE-001",
        source_occurrence_id=occ.occurrence_id,
        derived_assertion_id=derived_assertion_id,
        transformation_id=trans.transformation_id,
        confidence=1.0
    )

    # 4. Construct SourceGenealogy and verify reconstructability
    genealogy = SourceGenealogy(
        assertion_id=derived_assertion_id,
        edges=[edge],
        transformations=[trans],
        occurrences=[occ],
        artifacts=[artifact]
    )

    assert genealogy.is_reconstructable() is True
    assert occ.locator.locator_type == LocatorType.FILE_OFFSET
    assert occ.locator.uri == Path(f_path).resolve().as_uri()

    store.close()
    Path(f_path).unlink()
