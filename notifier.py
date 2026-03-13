from plyer import notification

def notify(file_name, folder_name):
    notification.notify(
        title="Sortify - File Moved",
        message=f"{file_name} moved to {folder_name}",
        timeout=5
    )