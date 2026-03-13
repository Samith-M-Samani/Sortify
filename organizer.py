"""Organize files based on extension rules.

This module contains the logic to move files into target folders based on their
file extension.
"""

from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)


def resolve_conflict(dst_path: Path) -> Path:
    """If the destination exists, find a non-conflicting path by adding a numeric suffix."""

    if not dst_path.exists():
        return dst_path

    parent = dst_path.parent
    stem = dst_path.stem
    suffix = dst_path.suffix

    counter = 1
    while True:
        candidate = parent / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def get_destination_folder(watch_folder: Path, extension: str, rules: Dict[str, str]) -> Optional[Path]:
    """Return the destination folder for a given extension using the configured rules."""

    normalized = extension.lower()
    dest = rules.get(normalized) or rules.get(normalized.lstrip("."))
    if not dest:
        return None

    return (watch_folder / dest).resolve()


def organize_file(
    src_path: str,
    watch_folder: str,
    rules: Dict[str, str],
    db: Optional["Database"] = None,
) -> Optional[str]:
    """Move a file based on extension rules and optionally log the move.

    Returns the destination path if the file was moved, or None otherwise.
    """

    src = Path(src_path)
    if not src.is_file():
        logger.debug("Skipping non-file: %s", src_path)
        return None

    extension = src.suffix.lower()
    dst_dir = get_destination_folder(Path(watch_folder), extension, rules)
    if dst_dir is None:
        logger.debug("No rule for extension %s (file: %s)", extension, src_path)
        return None

    dst_dir.mkdir(parents=True, exist_ok=True)
    dst_path = resolve_conflict(dst_dir / src.name)

    try:
        shutil.move(str(src), str(dst_path))
        logger.info("Moved %s -> %s", src, dst_path)

        if db is not None:
            try:
                db.log_move(str(src), str(dst_path), status="moved")
            except Exception as e:
                logger.warning("Failed to log move in DB: %s", e)

        return str(dst_path)
    except Exception as e:
        logger.exception("Failed to move file %s: %s", src, e)
        if db is not None:
            try:
                db.log_move(str(src), str(dst_path), status=f"error: {e}")
            except Exception:
                pass
        return None
