#!/usr/bin/env python3
"""Test script for basic notifications in Sortify."""

from notifier import send_basic_notification
import time

def test_basic_notifications():
    """Test sending various basic notifications."""

    print("Testing Sortify Basic Notifications")
    print("=" * 40)

    # Test startup notification
    send_basic_notification(
        "Sortify: Application Started",
        "Sortify file organizer is now running"
    )
    print("✓ Startup notification sent")

    time.sleep(1)

    # Test file creation notification
    send_basic_notification(
        "Sortify: File Created",
        "New file detected: document.pdf"
    )
    print("✓ File creation notification sent")

    time.sleep(1)

    # Test file organization notification
    send_basic_notification(
        "Sortify: File Organized",
        "Moved document.pdf to Documents/PDFs/"
    )
    print("✓ File organization notification sent")

    time.sleep(1)

    # Test file modification notification
    send_basic_notification(
        "Sortify: File Modified",
        "File modified: image.jpg"
    )
    print("✓ File modification notification sent")

    time.sleep(1)

    # Test file deletion notification
    send_basic_notification(
        "Sortify: File Deleted",
        "File deleted: temp.tmp"
    )
    print("✓ File deletion notification sent")

    time.sleep(1)

    # Test watcher started notification
    send_basic_notification(
        "Sortify: Watcher Started",
        "Monitoring folder: ./watch"
    )
    print("✓ Watcher started notification sent")

    print("\nAll basic notifications sent successfully!")
    print("Check your system notifications or console output.")

if __name__ == "__main__":
    test_basic_notifications()