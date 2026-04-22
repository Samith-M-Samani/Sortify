import os
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from organizer import organize_file
from notifier import notify

observer = None

class FileHandler(FileSystemEventHandler):
    def __init__(self, destination, log_callback, move_callback=None):
        self.destination = destination
        self.log_callback = log_callback
        self.move_callback = move_callback

    def on_created(self, event):
        if event.is_directory:
            return
        original_path = event.src_path
        new_path = organize_file(original_path, self.destination)
        file_name = os.path.basename(new_path)
        folder_name = os.path.basename(os.path.dirname(new_path))

        # Update GUI log via callback
        if callable(self.log_callback):
            self.log_callback(f"Moved: {file_name} → {folder_name}")

        # Call optional move callback (for revert handling, etc.)
        if callable(self.move_callback):
            self.move_callback(file_name, original_path, new_path)

        # Send notification
        notify(file_name, folder_name)


def start_watcher(monitor_folder, destination_folder, log_callback, move_callback=None):
    global observer
    if observer:
        return  # already running

    # Process any existing files immediately when sorting starts.
    scan_existing_files(monitor_folder, destination_folder, log_callback)

    event_handler = FileHandler(destination_folder, log_callback, move_callback)
    observer = Observer()
    observer.schedule(event_handler, monitor_folder, recursive=False)
    observer_thread = threading.Thread(target=observer.start)
    observer_thread.daemon = True
    observer_thread.start()


def scan_existing_files(monitor_folder, destination_folder, log_callback):
    if not os.path.isdir(monitor_folder):
        return

    for entry in os.listdir(monitor_folder):
        source_path = os.path.join(monitor_folder, entry)
        if os.path.isfile(source_path):
            try:
                new_path = organize_file(source_path, destination_folder)
                file_name = os.path.basename(new_path)
                folder_name = os.path.basename(os.path.dirname(new_path))
                if callable(log_callback):
                    log_callback(f"Existing file moved: {file_name} → {folder_name}")
            except Exception as err:
                if callable(log_callback):
                    log_callback(f"Error moving existing file '{entry}': {err}")


def stop_watcher():
    global observer
    if observer:
        observer.stop()
        observer.join()
        observer = None