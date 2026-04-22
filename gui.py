import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from watcher import start_watcher, stop_watcher

class SortifyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sortify - Smart File Organizer")
        self.root.geometry("600x400")

        # Folder to Monitor
        tk.Label(root, text="Folder to Monitor:").pack(pady=(10, 0))
        self.monitor_entry = tk.Entry(root, width=60)
        self.monitor_entry.pack(pady=5)
        tk.Button(root, text="Browse", command=self.browse_monitor).pack()

        # Destination Folder
        tk.Label(root, text="Destination Folder:").pack(pady=(10, 0))
        self.destination_entry = tk.Entry(root, width=60)
        self.destination_entry.pack(pady=5)
        tk.Button(root, text="Browse", command=self.browse_destination).pack()

        # Start/Stop Buttons
        tk.Button(root, text="Start Sorting", bg="green", fg="white",
                  command=self.start_sorting).pack(pady=(20, 5))
        tk.Button(root, text="Stop Sorting", bg="red", fg="white",
                  command=self.stop_sorting).pack(pady=5)

        # Activity Log
        tk.Label(root, text="Recent Activity:").pack(pady=(20, 0))
        self.activity_log = scrolledtext.ScrolledText(root, width=70, height=10)
        self.activity_log.pack(pady=5)

    def browse_monitor(self):
        folder = filedialog.askdirectory()
        if folder:
            self.monitor_entry.delete(0, tk.END)
            self.monitor_entry.insert(0, folder)

    def browse_destination(self):
        folder = filedialog.askdirectory()
        if folder:
            self.destination_entry.delete(0, tk.END)
            self.destination_entry.insert(0, folder)

    def start_sorting(self):
        monitor_folder = self.monitor_entry.get()
        destination_folder = self.destination_entry.get()

        if not monitor_folder or not destination_folder:
            messagebox.showwarning("Warning", "Please select both folders!")
            return

        self.activity_log.insert(tk.END, "Sorting started...\n")
        self.activity_log.see(tk.END)

        start_watcher(monitor_folder, destination_folder, self.activity_log)

    def stop_sorting(self):
        stop_watcher()
        self.activity_log.insert(tk.END, "Sorting stopped.\n")
        self.activity_log.see(tk.END)