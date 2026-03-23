"""Folder watcher for Sortify.

This module watches a folder for newly created files and triggers the organizer
logic to move files based on configured extension rules.
"""

from __future__ import annotations

import logging
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional

from watchdog.events import (
    FileSystemEventHandler,
    FileCreatedEvent,
    FileModifiedEvent,
    FileDeletedEvent,
    FileMovedEvent,
)
from watchdog.observers import Observer

from notifier import send_basic_notification, notify_event

logger = logging.getLogger(__name__)


class SortifyEventHandler(FileSystemEventHandler):
    def __init__(
        self,
        watch_folder: str,
        ignored_extensions: List[str],
        rules: Dict[str, str],
        db: Optional["Database"] = None,
        settle_time: float = 2.0,
    ):
        self.watch_folder = Path(watch_folder)
        self.ignored_extensions = {ext.lower() for ext in ignored_extensions}
        self.rules = rules
        self.db = db
        self.settle_time = settle_time
        super().__init__()

    def _is_ignored(self, path: Path) -> bool:
        return path.suffix.lower() in self.ignored_extensions

    def _wait_for_stable_file(self, path: Path) -> bool:
        """Wait for a file to stop changing size before processing."""

        try:
            last_size = path.stat().st_size
        except (FileNotFoundError, PermissionError):
            return False

        time.sleep(self.settle_time)

        try:
            current_size = path.stat().st_size
        except (FileNotFoundError, PermissionError):
            return False

        return current_size == last_size

    def _process(self, src_path: str) -> None:
        path = Path(src_path)

        if not path.is_file():
            return

        if self._is_ignored(path):
            logger.debug("Ignoring temporary file: %s", path)
            return

        if not self._wait_for_stable_file(path):
            logger.debug("File not stable or disappeared before organizing: %s", path)
            return

        # Send basic notification for file creation
        send_basic_notification(
            "Sortify: File Created",
            f"New file detected: {path.name}"
        )

        # For now, just log that we would organize the file
        logger.info("Would organize file: %s", path)

    def on_created(self, event: FileCreatedEvent) -> None:
        if event.is_directory:
            return

        threading.Thread(target=self._process, args=(event.src_path,), daemon=True).start()

    def on_modified(self, event: FileModifiedEvent) -> None:
        if event.is_directory:
            return

        path = Path(event.src_path)
        if self._is_ignored(path):
            return

        send_basic_notification(
            "Sortify: File Modified",
            f"File modified: {path.name}"
        )

    def on_deleted(self, event: FileDeletedEvent) -> None:
        if event.is_directory:
            return

        path = Path(event.src_path)
        if self._is_ignored(path):
            return

        send_basic_notification(
            "Sortify: File Deleted",
            f"File deleted: {path.name}"
        )

    def on_moved(self, event: FileMovedEvent) -> None:
        if event.is_directory:
            return

        src_path = Path(event.src_path)
        dest_path = Path(event.dest_path)
        if self._is_ignored(src_path) or self._is_ignored(dest_path):
            return

        send_basic_notification(
            "Sortify: File Moved",
            f"File moved: {src_path.name} -> {dest_path.name}"
        )


def start_watcher(
    watch_folder: str,
    ignored_extensions: List[str],
    rules: Dict[str, str],
    db: Optional["Database"] = None,
    stop_event: Optional[threading.Event] = None,
) -> Observer:
    """Start the watchdog observer and return it."""

    watch_folder_path = Path(watch_folder)
    watch_folder_path.mkdir(parents=True, exist_ok=True)

    event_handler = SortifyEventHandler(
        watch_folder=str(watch_folder_path),
        ignored_extensions=ignored_extensions,
        rules=rules,
        db=db,
    )

    observer = Observer()
    observer.schedule(event_handler, str(watch_folder_path), recursive=False)
    observer.start()

    # Send basic notification that watcher started
    send_basic_notification(
        "Sortify: Watcher Started",
        f"Monitoring folder: {watch_folder_path}"
    )

    logger.info("Started watcher on %s", watch_folder_path)

    if stop_event is not None:
        # Keep running until stop_event is set
        try:
            while not stop_event.is_set():
                time.sleep(0.5)
        except KeyboardInterrupt:
            logger.info("Received KeyboardInterrupt, stopping watcher")
        finally:
            observer.stop()
            observer.join()

    return observer
