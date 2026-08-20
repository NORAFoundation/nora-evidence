from datetime import datetime, timezone
import pytest
from nora_evidence.contracts import (
    AcquisitionEvent,
    Artifact,
    BasisEdge,
    Locator,
    LocatorType,
    SourceGenealogy,
    SourceOccurrence,
    Transformation,
    TransformationType
)

def test_canonical_contracts_and_reconstructability():
    acq = AcquisitionEvent(
        event_id="ACQ-001",
        source_channel="synthetic_upload",
        custodian="custodian@example.com",
        hash_value="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    
    art = Artifact(
        artifact_id="ART-001",
        mime_type="application/pdf",
        byte_size=1024,
        content_hash=acq.hash_value,
        acquisition=acq
    )
    
    loc = Locator(
        locator_type=LocatorType.PAGE_SPAN,
        uri="file:///synthetic/doc.pdf",
        start=1,
        end=2,
        context_snippet="Synthetic exhibit text"
    )
    
    occ = SourceOccurrence(
        occurrence_id="OCC-001",
        artifact_id=art.artifact_id,
        locator=loc,
        raw_content="Synthetic exhibit text"
    )
    
    trans = Transformation(
        transformation_id="TRANS-001",
        transformation_type=TransformationType.OCR_EXTRACT,
        input_occurrence_ids=[occ.occurrence_id],
        performed_by="nora-evidence-ocr-v1"
    )
    
    edge = BasisEdge(
        edge_id="EDGE-001",
        source_occurrence_id=occ.occurrence_id,
        derived_assertion_id="ASSERTION-999",
        transformation_id=trans.transformation_id
    )
    
    genealogy = SourceGenealogy(
        assertion_id="ASSERTION-999",
        edges=[edge],
        transformations=[trans],
        occurrences=[occ],
        artifacts=[art]
    )
    
    assert genealogy.is_reconstructable() is True
