from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional
from nora_evidence.contracts import Artifact, SourceOccurrence
from nora_evidence.custody import CustodyChain, CustodyRecord


class LocalEvidenceStore:
    """
    Local SQLite + FTS5 evidence store for offline-first record preservation,
    durable custody event persistence, and text search.
    """

    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self) -> None:
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS artifacts (
                    artifact_id TEXT PRIMARY KEY,
                    mime_type TEXT,
                    byte_size INTEGER,
                    content_hash TEXT,
                    acquired_at TEXT,
                    custodian TEXT
                )
            """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS occurrences (
                    occurrence_id TEXT PRIMARY KEY,
                    artifact_id TEXT,
                    uri TEXT,
                    raw_content TEXT,
                    FOREIGN KEY(artifact_id) REFERENCES artifacts(artifact_id)
                )
            """
            )
            self.conn.execute(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS occurrences_fts USING fts5(
                    occurrence_id UNINDEXED,
                    raw_content
                )
            """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS custody_events (
                    record_id TEXT PRIMARY KEY,
                    artifact_id TEXT,
                    action TEXT,
                    actor TEXT,
                    timestamp TEXT,
                    previous_hash TEXT,
                    record_hash TEXT,
                    FOREIGN KEY(artifact_id) REFERENCES artifacts(artifact_id)
                )
            """
            )

    def insert_artifact(self, artifact: Artifact) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO artifacts VALUES (?, ?, ?, ?, ?, ?)",
                (
                    artifact.artifact_id,
                    artifact.mime_type,
                    artifact.byte_size,
                    artifact.content_hash,
                    artifact.acquisition.acquired_at.isoformat(),
                    artifact.acquisition.custodian,
                ),
            )

    def insert_occurrence(self, occ: SourceOccurrence) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO occurrences VALUES (?, ?, ?, ?)",
                (
                    occ.occurrence_id,
                    occ.artifact_id,
                    occ.locator.uri,
                    occ.raw_content,
                ),
            )
            self.conn.execute(
                "INSERT OR REPLACE INTO occurrences_fts VALUES (?, ?)",
                (occ.occurrence_id, occ.raw_content),
            )

    def insert_custody_record(self, rec: CustodyRecord) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO custody_events VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    rec.record_id,
                    rec.artifact_id,
                    rec.action,
                    rec.actor,
                    rec.timestamp.isoformat(),
                    rec.previous_hash,
                    rec.record_hash,
                ),
            )

    def fetch_custody_chain(self, artifact_id: str) -> CustodyChain:
        cursor = self.conn.execute(
            """
            SELECT record_id, artifact_id, action, actor, timestamp, previous_hash, record_hash
            FROM custody_events
            WHERE artifact_id = ?
            ORDER BY rowid ASC
            """,
            (artifact_id,),
        )
        chain = CustodyChain(artifact_id=artifact_id)
        for row in cursor.fetchall():
            rec = CustodyRecord(
                record_id=row[0],
                artifact_id=row[1],
                action=row[2],
                actor=row[3],
                timestamp=datetime.fromisoformat(row[4]),
                previous_hash=row[5],
                record_hash=row[6],
            )
            chain.records.append(rec)
        return chain

    def search_occurrences(self, query: str) -> List[str]:
        cursor = self.conn.execute(
            "SELECT occurrence_id FROM occurrences_fts WHERE occurrences_fts MATCH ?",
            (query,),
        )
        return [row[0] for row in cursor.fetchall()]

    def close(self) -> None:
        self.conn.close()
