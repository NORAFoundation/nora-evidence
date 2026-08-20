import tempfile
from pathlib import Path
import pytest
from nora_evidence.extract import EvidenceExtractor

def test_evidence_extractor_text_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("Line 1: Synthetic record\nLine 2: Section assertion\n")
        f_path = f.name
        
    extractor = EvidenceExtractor()
    artifact, occurrences = extractor.extract_file(f_path)
    
    assert artifact.artifact_id.startswith("ART-")
    assert artifact.mime_type == "text/plain"
    assert len(occurrences) == 2
    assert occurrences[0].raw_content == "Line 1: Synthetic record"
    assert occurrences[1].raw_content == "Line 2: Section assertion"
    
    Path(f_path).unlink()
