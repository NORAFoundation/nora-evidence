from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field

GENESIS_HASH = "GENESIS_0000000000000000000000000000000000000000000000000000000000000000"


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
        prev_hash = self.records[-1].record_hash if self.records else GENESIS_HASH
        rec = CustodyRecord(
            record_id=record_id,
            artifact_id=self.artifact_id,
            action=action,
            actor=actor,
            previous_hash=prev_hash,
        )
        rec.record_hash = rec.compute_hash()
        self.records.append(rec)
        return rec

    def verify_chain(self) -> bool:
        if not self.records:
            return True
        expected_prev = GENESIS_HASH
        for rec in self.records:
            if rec.previous_hash != expected_prev:
                return False
            if rec.compute_hash() != rec.record_hash:
                return False
            expected_prev = rec.record_hash
        return True


class FileCustodyStore:
    """Durable file-backed store for custody chains."""

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self._chains: dict[str, CustodyChain] = {}
        self._load()

    def _load(self) -> None:
        if self.file_path.exists():
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for artifact_id, raw_chain in data.items():
                    self._chains[artifact_id] = CustodyChain.model_validate(raw_chain)

    def _save(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            data = {k: v.model_dump(mode="json") for k, v in self._chains.items()}
            json.dump(data, f, indent=2)

    def get_chain(self, artifact_id: str) -> CustodyChain:
        self._load()
        if artifact_id not in self._chains:
            self._chains[artifact_id] = CustodyChain(artifact_id=artifact_id)
        return self._chains[artifact_id]

    def save_chain(self, chain: CustodyChain) -> None:
        self._chains[chain.artifact_id] = chain
        self._save()
