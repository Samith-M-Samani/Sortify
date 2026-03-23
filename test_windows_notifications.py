#!/usr/bin/env python3
"""Test Windows notifications for Sortify."""

from notifier import send_basic_notification
import time

def test_windows_notifications():
    """Test Windows notification functionality."""

    print("Testing Windows Notifications for Sortify")
    print("=" * 50)

    # Test basic notification
    print("Sending basic notification...")
    send_basic_notification(
        "Sortify: Test Notification",
        "This is a test Windows notification from Sortify!"
    )
    print("✓ Basic notification sent")

    time.sleep(2)

    # Test file-related notifications
    print("Sending file creation notification...")
    send_basic_notification(
        "Sortify: File Created",
        "New file detected: document.pdf"
    )
    print("✓ File creation notification sent")

    time.sleep(2)

    # Test organization notification
    print("Sending file organization notification...")
    send_basic_notification(
        "Sortify: File Organized",
        "Moved document.pdf to Documents/PDFs/"
    )
    print("✓ File organization notification sent")

    print("\n" + "=" * 50)
    print("Check your Windows notification area (bottom right corner)")
    print("You should see toast notifications popping up!")
    print("If you don't see them, make sure notifications are enabled in Windows Settings.")

if __name__ == "__main__":
    test_windows_notifications()