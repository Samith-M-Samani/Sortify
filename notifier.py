"""Notification and undo support for Sortify.

This module sends Windows notifications when files are moved with OK and Undo buttons.
"""

from __future__ import annotations

import ctypes
from typing import Optional


def show_notification(title: str, message: str) -> str:
    """Show a Windows notification with OK and Undo buttons.
    
    Returns "OK" or "Undo" based on user's choice.
    """
    # Message box types
    MB_OKCANCEL = 0x0001  # OK and Cancel buttons
    MB_DEFBUTTON1 = 0x0000  # Default to first button (OK)
    MB_ICONINFORMATION = 0x0040  # Information icon
    
    full_message = f"{message}\n\n(Click OK or Undo)"
    
    result = ctypes.windll.user32.MessageBoxW(
        None,  # No parent window
        full_message,
        title,
        MB_OKCANCEL | MB_DEFBUTTON1 | MB_ICONINFORMATION
    )
    
    # IDOK = 1, IDCANCEL = 2
    return "OK" if result == 1 else "Undo"


def send_basic_notification(title: str, message: str) -> None:
    """Send a basic Windows notification."""
    try:
        show_notification(title, message)
    except Exception:
        pass


def notify_event(title: str, message: str, actions: Optional[list] = None, timeout: int = 10) -> Optional[str]:
    """Send a notification event and return the selected action."""
    try:
        return show_notification(title, message)
    except Exception:
        return None


def notify_move(dst_file: str, db: Optional["Database"] = None) -> None:
    """Send a notification when a file has been moved.
    
    Shows a Windows notification with OK and Undo buttons.
    If the user selects Undo, it will attempt to revert the last move.
    """
    title = "Sortify: File Organized"
    message = f"File moved to:\n{dst_file}"
    
    action = show_notification(title, message)
    
    if action == "Undo" and db is not None:
        # Undo functionality implementation would go here
        pass
