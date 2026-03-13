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

from config import load_config
from database import Database
from watcher import start_watcher


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Sortify - Auto File Organizer")
    parser.add_argument(
        "--config",
        help="Path to configuration JSON file (default: ./config.json)",
        default=None,
    )
    parser.add_argument(
        "--db",
        help="Path to SQLite database file (default: filelog.db)",
        default=None,
    )
    parser.add_argument(
        "--log-level",
        help="Logging verbosity (DEBUG, INFO, WARNING, ERROR)",
        default="INFO",
    )
    args = parser.parse_args()

    configure_logging(args.log_level)
    logger = logging.getLogger(__name__)

    config = load_config(args.config)

    db = Database(db_path=args.db)

    stop_event = threading.Event()
    observer = start_watcher(
        watch_folder=config["watch_folder"],
        ignored_extensions=config["ignored_extensions"],
        rules=config["extension_rules"],
        db=db,
        stop_event=stop_event,
    )

    try:
        logger.info("Sortify is running. Press Ctrl+C to stop.")
        while not stop_event.is_set():
            time.sleep(0.5)
    except KeyboardInterrupt:
        logger.info("Interrupt received, shutting down...")
    finally:
        stop_event.set()
        observer.stop()
        observer.join()
        db.close()
        logger.info("Sortify has stopped.")


if __name__ == "__main__":
    main()
