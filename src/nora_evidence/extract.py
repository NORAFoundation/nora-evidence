from __future__ import annotations
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from nora_evidence.contracts import (
    AcquisitionEvent,
    Artifact,
    Locator,
    LocatorType,
    ReadinessScore,
    SourceOccurrence,
)

class EvidenceExtractor:
    """
    Multi-format extraction dispatcher that converts raw evidence files into
    tracked Artifacts and SourceOccurrences with exact locators.
    """
    def __init__(self, custodian: str = "system_extractor"):
        self.custodian = custodian

    def extract_file(self, file_path: str, mime_type: Optional[str] = None) -> tuple[Artifact, List[SourceOccurrence]]:
        path = Path(file_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Evidence file not found: {path}")

        raw_bytes = path.read_bytes()
        file_hash = hashlib.sha256(raw_bytes).hexdigest()
        byte_size = len(raw_bytes)
        
        inferred_mime = mime_type or self._infer_mime(path)
        
        acq = AcquisitionEvent(
            event_id=f"ACQ-{file_hash[:8]}",
            source_channel="local_ingest",
            custodian=self.custodian,
            hash_value=file_hash
        )
        
        art = Artifact(
            artifact_id=f"ART-{file_hash[:12]}",
            mime_type=inferred_mime,
            byte_size=byte_size,
            content_hash=file_hash,
            acquisition=acq
        )

        occurrences = []
        if inferred_mime.startswith("text/"):
            text_content = raw_bytes.decode("utf-8", errors="replace")
            lines = text_content.splitlines()
            for idx, line in enumerate(lines, start=1):
                if not line.strip():
                    continue
                loc = Locator(
                    locator_type=LocatorType.FILE_OFFSET,
                    uri=path.as_uri(),
                    start=idx,
                    end=idx,
                    context_snippet=line.strip()
                )
                occurrences.append(SourceOccurrence(
                    occurrence_id=f"OCC-{file_hash[:8]}-L{idx}",
                    artifact_id=art.artifact_id,
                    locator=loc,
                    raw_content=line.strip()
                ))
        else:
            loc = Locator(
                locator_type=LocatorType.URI,
                uri=path.as_uri(),
                context_snippet=f"Binary object: {path.name}"
            )
            occurrences.append(SourceOccurrence(
                occurrence_id=f"OCC-{file_hash[:8]}-BIN",
                artifact_id=art.artifact_id,
                locator=loc,
                raw_content=f"BINARY_OBJECT:{path.name}:{file_hash}"
            ))

        return art, occurrences

    @staticmethod
    def _infer_mime(path: Path) -> str:
        suffix = path.suffix.lower()
        if suffix in {".txt", ".md", ".jsonl", ".csv"}:
            return "text/plain"
        elif suffix == ".pdf":
            return "application/pdf"
        elif suffix in {".png", ".jpg", ".jpeg"}:
            return "image/png"
        elif suffix in {".mp3", ".wav"}:
            return "audio/wav"
        return "application/octet-stream"
def compute_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def extract_evidence_artifact(file_path: str, custodian: str = "system_extractor") -> tuple[Artifact, List[SourceOccurrence]]:
    extractor = EvidenceExtractor(custodian=custodian)
    return extractor.extract_file(file_path)

def score_readiness(artifact: Artifact, occurrences: List[SourceOccurrence]) -> ReadinessScore:
    reasons = []
    if not artifact.content_hash:
        reasons.append("Missing content hash")
    if not occurrences:
        reasons.append("No occurrences extracted")
    is_ready = len(reasons) == 0
    score = 1.0 if is_ready else 0.0
    return ReadinessScore(
        artifact_id=artifact.artifact_id,
        is_ready=is_ready,
        score=score,
        reasons=reasons,
    )
