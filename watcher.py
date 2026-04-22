import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from organizer import organize_file
from notifier import Notifier   # ✅ FIXED IMPORT

observer = None


class FileHandler(FileSystemEventHandler):
    def __init__(self, destination, log_widget):
        self.destination = destination
        self.log_widget = log_widget
        self.notifier = Notifier()   # ✅ CREATE INSTANCE

    def on_created(self, event):
        if event.is_directory:
            return

        try:
            new_path = organize_file(event.src_path, self.destination)

            file_name = new_path.split("\\")[-1]
            folder_name = new_path.split("\\")[-2]

            # ✅ Update GUI log
            self.log_widget.insert("end", f"{file_name} → {folder_name}\n")
            self.log_widget.see("end")

            # ✅ Send notification (correct method)
            self.notifier.category(file_name, folder_name)
            self.notifier.success(file_name)

        except Exception as e:
            file_name = event.src_path.split("\\")[-1]
            self.notifier.error(file_name)
            print(f"Error processing file: {e}")


def start_watcher(monitor_folder, destination_folder, log_widget):
    global observer

    if observer:
        return  # already running

    event_handler = FileHandler(destination_folder, log_widget)

    observer = Observer()
    observer.schedule(event_handler, monitor_folder, recursive=False)

    # ✅ Threaded start (correct)
    observer_thread = threading.Thread(target=observer.start)
    observer_thread.daemon = True
    observer_thread.start()


def stop_watcher():
    global observer

    if observer:
        observer.stop()
        observer.join()
        observer = None