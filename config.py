"""Configuration loader for Sortify.

This module tries to load configuration from `config.json` (preferred), falling back to
hardcoded defaults if the JSON file does not exist or is invalid.

Configuration keys:
- watch_folder: Folder to monitor for new files.
- ignored_extensions: File extensions to ignore (temporary downloads, partials, etc.).
- extension_rules: Mapping of file extension to destination subfolder.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

DEFAULTS = {
    "watch_folder": str(Path(".").resolve()),
    "ignored_extensions": [".crdownload", ".part", ".tmp", ".partial"],
    "extension_rules": {
        ".pdf": "Documents/PDFs",
        ".docx": "Documents/Word",
        ".xlsx": "Documents/Excel",
        ".png": "Pictures/Images",
        ".jpg": "Pictures/Images",
        ".jpeg": "Pictures/Images",
        ".mp3": "Music",
        ".mp4": "Videos",
        ".zip": "Archives",
    },
}


def load_config(config_path: str | Path | None = None) -> Dict[str, Any]:
    """Load configuration for Sortify.

    Args:
        config_path: Optional explicit path to a JSON config file. If not provided,
            will look for `config.json` in the project root.

    Returns:
        dict: configuration dictionary.
    """

    if config_path is None:
        config_path = Path(__file__).resolve().parent / "config.json"
    else:
        config_path = Path(config_path)

    config: Dict[str, Any] = DEFAULTS.copy()

    if config_path.is_file():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict):
                raise ValueError("config.json must contain a JSON object")

            config.update({k: data[k] for k in data if k in config})
        except Exception as e:
            logger.warning("Failed to load config from %s: %s", config_path, e)

    # Normalize watch folder path
    config["watch_folder"] = str(Path(config["watch_folder"]).expanduser().resolve())

    return config
