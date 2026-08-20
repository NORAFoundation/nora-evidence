import pytest
from nora_evidence.contracts import (
    AcquisitionEvent,
    Artifact,
    Locator,
    LocatorType,
    SourceOccurrence
)
from nora_evidence.custody import CustodyChain
from nora_evidence.store import LocalEvidenceStore

def test_custody_chain_verification():
    chain = CustodyChain(artifact_id="ART-100")
    chain.append("REC-01", "INGEST", "agent-01")
    chain.append("REC-02", "TRANSFORM", "agent-02")
    
    assert len(chain.records) == 2
    assert chain.verify_chain() is True
    
    # Tamper with record hash
    chain.records[0].record_hash = "tampered_hash"
    assert chain.verify_chain() is False

def test_local_evidence_store_fts():
    store = LocalEvidenceStore(":memory:")
    acq = AcquisitionEvent(
        event_id="ACQ-100",
        source_channel="local",
        custodian="dev@example.com",
        hash_value="hash-100"
    )
    art = Artifact(
        artifact_id="ART-100",
        mime_type="text/plain",
        byte_size=50,
        content_hash="hash-100",
        acquisition=acq
    )
    occ = SourceOccurrence(
        occurrence_id="OCC-100",
        artifact_id=art.artifact_id,
        locator=Locator(locator_type=LocatorType.URI, uri="file:///test.txt"),
        raw_content="Synthetic testimony regarding agreement terms"
    )
    
    store.insert_artifact(art)
    store.insert_occurrence(occ)
    
    results = store.search_occurrences("agreement")
    assert "OCC-100" in results
    store.close()
