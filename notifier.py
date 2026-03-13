"""Notification and undo support for Sortify.

This module sends notifications when files are moved and supports undoing the most
recent move using the SQLite log.

The implementation tries to use `tlinker` for system notifications (with actionable
buttons), but it gracefully falls back to console logging if `tlinker` is not available.
"""

from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import Optional

from database import Database
from organizer import resolve_conflict

logger = logging.getLogger(__name__)

try:
    from tlinker import notify
except ImportError:  # pragma: no cover
    notify = None  # type: ignore


def undo_last_move(db: Database) -> bool:
    """Undo the last logged file move.

    Returns True if the undo succeeded, False otherwise.
    """

    last = db.get_last_move(only_successful=True)
    if not last:
        logger.debug("No move found to undo.")
        return False

    src = Path(last["dst_path"])
    dst = Path(last["src_path"])

    if not src.exists():
        logger.warning("Cannot undo move, file does not exist: %s", src)
        return False

    dst.parent.mkdir(parents=True, exist_ok=True)
    target = resolve_conflict(dst)

    try:
        shutil.move(str(src), str(target))
        logger.info("Undid move: %s -> %s", src, target)
        db.log_move(str(src), str(target), status="undone")
        return True
    except Exception as e:
        logger.exception("Failed to undo move %s -> %s: %s", src, dst, e)
        return False


def notify_move(dst_file: str, db: Optional[Database] = None) -> None:
    """Send a notification when a file has been moved.

    If `tlinker` is available, this will show an actionable notification with
    'Undo' and 'Done' options. If the user selects Undo, it will attempt to revert
    the last move using the database.
    """

    title = "Sortify: File Organized"
    message = f"Moved file to: {dst_file}"

    if notify is None:
        logger.info("%s - %s", title, message)
        return

    try:
        action = notify(
            title,
            message,
            actions=["Undo", "Done"],
            timeout=10,
        )

        if action == "Undo" and db is not None:
            if undo_last_move(db):
                logger.info("Undo succeeded for %s", dst_file)
            else:
                logger.warning("Undo failed for %s", dst_file)
    except Exception as e:  # pragma: no cover
        logger.exception("Failed to send notification: %s", e)
