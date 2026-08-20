from __future__ import annotations
import hashlib
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field

class CustodyRecord(BaseModel):
    record_id: str
    artifact_id: str
    action: str
    actor: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    previous_hash: str
    record_hash: str = ""

    def compute_hash(self) -> str:
        payload = f"{self.record_id}:{self.artifact_id}:{self.action}:{self.actor}:{self.timestamp.isoformat()}:{self.previous_hash}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

class CustodyChain(BaseModel):
    artifact_id: str
    records: List[CustodyRecord] = Field(default_factory=list)

    def append(self, record_id: str, action: str, actor: str) -> CustodyRecord:
        prev_hash = self.records[-1].record_hash if self.records else "GENESIS_0000000000000000000000000000000000000000000000000000000000000000"
        rec = CustodyRecord(
            record_id=record_id,
            artifact_id=self.artifact_id,
            action=action,
            actor=actor,
            previous_hash=prev_hash
        )
        rec.record_hash = rec.compute_hash()
        self.records.append(rec)
        return rec

    def verify_chain(self) -> bool:
        if not self.records:
            return True
        expected_prev = "GENESIS_0000000000000000000000000000000000000000000000000000000000000000"
        for rec in self.records:
            if rec.previous_hash != expected_prev:
                return False
            if rec.compute_hash() != rec.record_hash:
                return False
            expected_prev = rec.record_hash
        return True
