#!/usr/bin/env python3
"""Setup script for Sortify Windows notifications."""

import subprocess
import sys
import platform

def install_package(package_name):
    """Install a Python package using pip."""
    try:
        print(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✓ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package_name}: {e}")
        return False

def setup_windows_notifications():
    """Set up Windows notifications for Sortify."""

    print("Sortify - Windows Notification Setup")
    print("=" * 40)

    if platform.system() != "Windows":
        print("This setup is for Windows systems only.")
        print("For other systems, install tlinker: pip install tlinker")
        return

    print("Setting up Windows notifications...")
    print()

    # Try to install plyer (recommended)
    plyer_installed = install_package("plyer")

    if not plyer_installed:
        print("plyer installation failed. Trying win10toast...")
        win10toast_installed = install_package("win10toast")

        if not win10toast_installed:
            print("win10toast installation also failed.")
            print("Windows notifications will use PowerShell fallback.")
            print("This may have limited functionality.")
        else:
            print("✓ win10toast installed - you'll get Windows toast notifications!")
    else:
        print("✓ plyer installed - you'll get full Windows notifications!")

    print()
    print("Testing notifications...")

    # Test the notification
    try:
        if plyer_installed:
            from plyer import notification
            notification.notify(
                title="Sortify: Setup Complete",
                message="Windows notifications are now working!",
                app_name="Sortify",
                timeout=5
            )
        else:
            # Use PowerShell fallback
            ps_command = '''
            Add-Type -AssemblyName System.Windows.Forms
            $notify = New-Object System.Windows.Forms.NotifyIcon
            $notify.Icon = [System.Drawing.SystemIcons]::Information
            $notify.BalloonTipTitle = "Sortify: Setup Complete"
            $notify.BalloonTipText = "Windows notifications are now working!"
            $notify.BalloonTipIcon = "Info"
            $notify.Visible = $true
            $notify.ShowBalloonTip(5000)
            '''
            subprocess.run(["powershell", "-Command", ps_command], capture_output=True)

        print("✓ Test notification sent! Check your Windows notification area.")
    except Exception as e:
        print(f"✗ Test notification failed: {e}")

    print()
    print("Setup complete! You can now run Sortify with Windows notifications.")
    print("Run: python test_windows_notifications.py")

if __name__ == "__main__":
    setup_windows_notifications()