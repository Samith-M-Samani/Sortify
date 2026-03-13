"""SQLite database helper for Sortify.

This module provides a simple wrapper around `sqlite3` to store file move history and
extension rules. The database lives in `filelog.db` by default.

Tables:
- moves: records every file move operation (source, destination, timestamp).
- extension_rules: optional table to persist custom rules (not required for basic config).
"""

from __future__ import annotations

import datetime
import logging
import sqlite3
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Iterable, Optional, Tuple

logger = logging.getLogger(__name__)

DEFAULT_DB_PATH = Path("filelog.db")


class Database:
    def __init__(self, db_path: str | Path | None = None):
        self._path = Path(db_path) if db_path else DEFAULT_DB_PATH
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self._path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._lock = Lock()
        self._initialize()

    def _initialize(self) -> None:
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS moves (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    src_path TEXT NOT NULL,
                    dst_path TEXT NOT NULL,
                    status TEXT NOT NULL
                );
                """
            )
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS extension_rules (
                    extension TEXT PRIMARY KEY,
                    destination TEXT NOT NULL
                );
                """
            )

    def log_move(self, src_path: str, dst_path: str, status: str = "moved") -> None:
        """Log a file move operation."""

        timestamp = datetime.datetime.utcnow().isoformat() + "Z"
        with self._lock, self._conn:
            self._conn.execute(
                "INSERT INTO moves (timestamp, src_path, dst_path, status) VALUES (?, ?, ?, ?)",
                (timestamp, src_path, dst_path, status),
            )
        logger.debug("Logged move: %s -> %s (%s)", src_path, dst_path, status)

    def get_last_move(self, only_successful: bool = True) -> Optional[Dict[str, str]]:
        """Return the most recent file move entry.

        Args:
            only_successful: If True, only returns moves with status 'moved'.

        Returns:
            A dict with keys (id, timestamp, src_path, dst_path, status), or None if no record.
        """

        query = "SELECT id, timestamp, src_path, dst_path, status FROM moves"
        params: tuple = ()
        if only_successful:
            query += " WHERE status = ?"
            params = ("moved",)
        query += " ORDER BY id DESC LIMIT 1"

        with self._lock:
            cursor = self._conn.execute(query, params)
            row = cursor.fetchone()
            if not row:
                return None
            return {
                "id": row["id"],
                "timestamp": row["timestamp"],
                "src_path": row["src_path"],
                "dst_path": row["dst_path"],
                "status": row["status"],
            }

    def get_extension_rules(self) -> Dict[str, str]:
        """Return extension rules saved in the database."""
        with self._lock:
            cursor = self._conn.execute("SELECT extension, destination FROM extension_rules")
            return {row["extension"]: row["destination"] for row in cursor.fetchall()}

    def upsert_extension_rule(self, extension: str, destination: str) -> None:
        """Add or update an extension rule."""
        with self._lock, self._conn:
            self._conn.execute(
                "INSERT INTO extension_rules (extension, destination) VALUES (?, ?)"
                " ON CONFLICT(extension) DO UPDATE SET destination = excluded.destination",
                (extension.lower(), destination),
            )
        logger.debug("Upserted extension rule: %s -> %s", extension, destination)

    def remove_extension_rule(self, extension: str) -> None:
        """Remove an extension rule."""
        with self._lock, self._conn:
            self._conn.execute(
                "DELETE FROM extension_rules WHERE extension = ?",
                (extension.lower(),),
            )
        logger.debug("Removed extension rule: %s", extension)

    def close(self) -> None:
        """Close the underlying database connection."""
        self._conn.close()
