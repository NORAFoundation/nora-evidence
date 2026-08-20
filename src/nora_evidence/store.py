from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import List, Optional
from nora_evidence.contracts import Artifact, SourceOccurrence

class LocalEvidenceStore:
    """
    Local SQLite + FTS5 evidence store for offline-first record preservation and text search.
    """
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self) -> None:
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS artifacts (
                    artifact_id TEXT PRIMARY KEY,
                    mime_type TEXT,
                    byte_size INTEGER,
                    content_hash TEXT,
                    acquired_at TEXT,
                    custodian TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS occurrences (
                    occurrence_id TEXT PRIMARY KEY,
                    artifact_id TEXT,
                    uri TEXT,
                    raw_content TEXT,
                    FOREIGN KEY(artifact_id) REFERENCES artifacts(artifact_id)
                )
            """)
            self.conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS occurrences_fts USING fts5(
                    occurrence_id UNINDEXED,
                    raw_content
                )
            """)

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
                    artifact.acquisition.custodian
                )
            )

    def insert_occurrence(self, occ: SourceOccurrence) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO occurrences VALUES (?, ?, ?, ?)",
                (
                    occ.occurrence_id,
                    occ.artifact_id,
                    occ.locator.uri,
                    occ.raw_content
                )
            )
            self.conn.execute(
                "INSERT OR REPLACE INTO occurrences_fts VALUES (?, ?)",
                (occ.occurrence_id, occ.raw_content)
            )

    def search_occurrences(self, query: str) -> List[str]:
        cursor = self.conn.execute(
            "SELECT occurrence_id FROM occurrences_fts WHERE occurrences_fts MATCH ?",
            (query,)
        )
        return [row[0] for row in cursor.fetchall()]

    def close(self) -> None:
        self.conn.close()
