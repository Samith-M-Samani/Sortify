#!/usr/bin/env python3
"""Entry point for Sortify - Auto File Organizer.

This module initializes the SQLite database, loads configuration, and starts the
background watcher service. It is intended to run continuously to monitor a folder
in real-time and organize newly created files.
"""

from __future__ import annotations

import argparse
import logging
import threading
import time

from notifier import send_basic_notification
from watcher import start_watcher

def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s %(name)s: %(message)s",
    )

def main() -> None:
    parser = argparse.ArgumentParser(description="Sortify - Auto File Organizer")
    parser.add_argument(
        "--config",
        help="Path to configuration JSON file (default: ./config.json)",
        default="./config.json",
    )
    parser.add_argument(
        "--log-level",
        help="Logging verbosity (DEBUG, INFO, WARNING, ERROR)",
        default="INFO",
    )
    args = parser.parse_args()

    configure_logging(args.log_level)
    logger = logging.getLogger(__name__)

    # Send startup notification
    send_basic_notification(
        "Sortify: Starting Up",
        "Initializing Sortify file organizer..."
    )

    # For now, use basic config
    watch_folder = "./watch"
    ignored_extensions = [".crdownload", ".part", ".tmp", ".partial"]
    rules = {
        ".pdf": "Documents/PDFs",
        ".docx": "Documents/Word",
        ".xlsx": "Documents/Excel",
        ".png": "Pictures/Images",
        ".jpg": "Pictures/Images",
        ".jpeg": "Pictures/Images",
        ".mp3": "Music",
        ".mp4": "Videos",
        ".zip": "Archives"
    }

    stop_event = threading.Event()
    observer = start_watcher(
        watch_folder=watch_folder,
        ignored_extensions=ignored_extensions,
        rules=rules,
        stop_event=stop_event,
    )

    try:
        logger.info("Sortify is running. Press Ctrl+C to stop.")
        send_basic_notification(
            "Sortify: Running",
            f"Monitoring folder: {watch_folder}"
        )
        while not stop_event.is_set():
            time.sleep(0.5)
    except KeyboardInterrupt:
        logger.info("Interrupt received, shutting down...")
        send_basic_notification(
            "Sortify: Shutting Down",
            "Stopping file organizer..."
        )
    finally:
        stop_event.set()
        observer.stop()
        observer.join()
        send_basic_notification(
            "Sortify: Stopped",
            "File organizer has stopped"
        )
        logger.info("Sortify has stopped.")

if __name__ == "__main__":
    main()
