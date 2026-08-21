from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class HashAlgorithm(str, Enum):
    SHA256 = "sha256"
    SHA512 = "sha512"

class LocatorType(str, Enum):
    FILE_OFFSET = "file_offset"
    PAGE_SPAN = "page_span"
    TEXT_SPAN = "text_span"
    AUDIO_TIMESTAMP = "audio_timestamp"
    URI = "uri"

class Locator(BaseModel):
    locator_type: LocatorType
    uri: str
    start: Optional[Any] = None
    end: Optional[Any] = None
    context_snippet: Optional[str] = None

class AcquisitionEvent(BaseModel):
    event_id: str
    source_channel: str
    acquired_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    custodian: str
    hash_value: str
    hash_algorithm: HashAlgorithm = HashAlgorithm.SHA256

class Artifact(BaseModel):
    artifact_id: str
    mime_type: str
    byte_size: int
    content_hash: str
    acquisition: AcquisitionEvent
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_connector_envelope(cls, envelope: Any) -> Artifact:
        env_id = getattr(envelope, "envelope_id", "env-001")
        sha256 = getattr(envelope, "sha256", "") or ""
        size = getattr(envelope, "size_bytes", 0)
        locator = getattr(envelope, "locator", "")
        acq = AcquisitionEvent(
            event_id=f"ACQ-{env_id}",
            source_channel="connector",
            custodian="system",
            hash_value=sha256,
        )
        return cls(
            artifact_id=f"ART-{env_id}",
            mime_type="text/plain" if str(locator).endswith((".txt", ".md")) else "application/octet-stream",
            byte_size=size,
            content_hash=sha256,
            acquisition=acq,
            metadata={"locator": locator},
        )

class ReadinessScore(BaseModel):
    artifact_id: str
    is_ready: bool
    score: float
    reasons: List[str] = Field(default_factory=list)
class SourceOccurrence(BaseModel):
    occurrence_id: str
    artifact_id: str
    locator: Locator
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    raw_content: str

class TransformationType(str, Enum):
    OCR_EXTRACT = "ocr_extract"
    AUDIO_TRANSCRIBE = "audio_transcribe"
    TEXT_NORMALIZE = "text_normalize"
    CLAIMS_PARSED = "claims_parsed"

class Transformation(BaseModel):
    transformation_id: str
    transformation_type: TransformationType
    input_occurrence_ids: List[str]
    performed_by: str
    performed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    parameters: Dict[str, Any] = Field(default_factory=dict)

class BasisEdge(BaseModel):
    edge_id: str
    source_occurrence_id: str
    derived_assertion_id: str
    transformation_id: str
    confidence: float = 1.0

class SourceGenealogy(BaseModel):
    assertion_id: str
    edges: List[BasisEdge] = Field(default_factory=list)
    transformations: List[Transformation] = Field(default_factory=list)
    occurrences: List[SourceOccurrence] = Field(default_factory=list)
    artifacts: List[Artifact] = Field(default_factory=list)

    def is_reconstructable(self) -> bool:
        if not self.edges:
            return False
        occ_ids = {o.occurrence_id for o in self.occurrences}
        trans_ids = {t.transformation_id for t in self.transformations}
        
        for edge in self.edges:
            if edge.source_occurrence_id not in occ_ids:
                return False
            if edge.transformation_id not in trans_ids:
                return False
        return True
