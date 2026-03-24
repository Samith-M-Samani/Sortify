from plyer import notification


def notify(file_name, folder_name):
    # System notification: include instruction for manual revert using GUI.
    notification.notify(
        title="Sortify - File Moved",
        message=(f"{file_name} moved to {folder_name}. "
                 "Open Sortify and use 'Revert Last' to send it back."),
        timeout=5
    )