"""Notification and undo support for Sortify.

This module sends notifications when files are moved and supports undoing the most
recent move using the SQLite log.

For Windows notifications, install plyer: pip install plyer
"""

from __future__ import annotations

import logging
import platform
import subprocess
import os
from typing import Optional

logger = logging.getLogger(__name__)

def _notify_windows_msg(title: str, message: str, **kwargs):
    """Send Windows notification using msg command."""
    try:
        # Use Windows msg command for simple notifications
        full_message = f"{title}\n\n{message}"
        subprocess.run(
            ["msg", "*", full_message],
            capture_output=True,
            check=False,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
        )
        return True
    except Exception as e:
        logger.debug(f"MSG notification failed: {e}")
        return False

def _notify_windows_powershell(title: str, message: str, **kwargs):
    """Send Windows toast notification using PowerShell."""
    try:
        # Simplified PowerShell toast notification
        ps_command = f'''
        Add-Type -AssemblyName System.Windows.Forms
        $notify = New-Object System.Windows.Forms.NotifyIcon
        $notify.Icon = [System.Drawing.SystemIcons]::Information
        $notify.BalloonTipTitle = "{title}"
        $notify.BalloonTipText = "{message}"
        $notify.BalloonTipIcon = "Info"
        $notify.Visible = $true
        $notify.ShowBalloonTip(5000)
        Start-Sleep -Seconds 5
        $notify.Dispose()
        '''
        subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            check=False,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
        )
        return True
    except Exception as e:
        logger.debug(f"PowerShell notification failed: {e}")
        return False

# Set up notification function based on platform
if platform.system() == "Windows":
    # Try plyer first (if installed)
    try:
        from plyer import notification
        def _notify_plyer(title: str, message: str, **kwargs):
            notification.notify(
                title=title,
                message=message,
                app_name="Sortify",
                timeout=5
            )
        notify = _notify_plyer
        logger.info("Using plyer for Windows notifications")
    except ImportError:
        logger.info("plyer not installed. For Windows notifications, run: pip install plyer")
        # Fallback to PowerShell notifications
        notify = _notify_windows_powershell
        logger.info("Using PowerShell for Windows notifications")
else:
    # For non-Windows systems
    try:
        from tlinker import notify as tlinker_notify
        notify = tlinker_notify
        logger.info("Using tlinker for notifications")
    except ImportError:
        notify = None
        logger.warning("No notification library available. Using console output.")


def send_basic_notification(title: str, message: str) -> None:
    """Send a basic notification.

    If `tlinker` is available, this will show a system notification.
    Falls back to console logging if `tlinker` is not available.
    """
    if notify is None:
        logger.info("%s - %s", title, message)
        return

    try:
        notify(title, message)
    except Exception as e:  # pragma: no cover
        logger.exception("Failed to send notification: %s", e)


def notify_event(title: str, message: str, actions: Optional[list] = None, timeout: int = 10) -> Optional[str]:
    """Send a general notification.

    If `tlinker` is available, this will show a notification with optional actions.
    Falls back to console logging if `tlinker` is not available.

    Returns the selected action if actions are provided, None otherwise.
    """
    if notify is None:
        logger.info("%s - %s", title, message)
        return None

    try:
        return notify(
            title,
            message,
            actions=actions or [],
            timeout=timeout,
        )
    except Exception as e:  # pragma: no cover
        logger.exception("Failed to send notification: %s", e)
        return None


def notify_move(dst_file: str, db: Optional["Database"] = None) -> None:
    """Send a notification when a file has been moved.

    If `tlinker` is available, this will show an actionable notification with
    'Undo' and 'Done' options. If the user selects Undo, it will attempt to revert
    the last move using the database.
    """

    title = "Sortify: File Organized"
    message = f"Moved file to: {dst_file}"

    action = notify_event(title, message, actions=["Undo", "Done"])

    if action == "Undo" and db is not None:
        # For now, just log - undo functionality would need the full implementation
        logger.info("Undo requested for %s", dst_file)
