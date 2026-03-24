import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from watcher import start_watcher, stop_watcher
from organizer import revert_file
from database import mark_file_reverted

class SortifyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sortify - Sortify: Smart File Organizer")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TLabel", font=("Segoe UI", 10), foreground="#2b2b2b")
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)

        # Menu bar
        menubar = tk.Menu(root)
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        root.config(menu=menubar)

        self.main_frame = ttk.Frame(root, padding=(15, 15, 15, 15))
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.last_move = None

        header = ttk.Label(self.main_frame, text="Sortify", font=("Segoe UI", 16, "bold"))
        header.grid(row=0, column=0, columnspan=3, sticky="w")

        subtitle = ttk.Label(self.main_frame, text="Smartly monitor and organize your downloads folder")
        subtitle.grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 15))

        ttk.Label(self.main_frame, text="Folder to Monitor:").grid(row=2, column=0, sticky="w", pady=(0, 4))
        self.monitor_entry = ttk.Entry(self.main_frame, width=55)
        self.monitor_entry.grid(row=3, column=0, columnspan=2, sticky="w")
        ttk.Button(self.main_frame, text="Browse", command=self.browse_monitor, width=12).grid(row=3, column=2, sticky="e")

        ttk.Label(self.main_frame, text="Destination Folder:").grid(row=4, column=0, sticky="w", pady=(10, 4))
        self.destination_entry = ttk.Entry(self.main_frame, width=55)
        self.destination_entry.grid(row=5, column=0, columnspan=2, sticky="w")
        ttk.Button(self.main_frame, text="Browse", command=self.browse_destination, width=12).grid(row=5, column=2, sticky="e")

        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=(20, 8), sticky="ew")

        self.start_button = ttk.Button(button_frame, text="Start Sorting", command=self.start_sorting, style="Accent.TButton")
        self.start_button.grid(row=0, column=0, padx=(0, 10))

        self.stop_button = ttk.Button(button_frame, text="Stop Sorting", command=self.stop_sorting)
        self.stop_button.grid(row=0, column=1, padx=(0, 10))
        self.stop_button.state(["disabled"])

        self.clear_button = ttk.Button(button_frame, text="Clear Log", command=self.clear_log)
        self.clear_button.grid(row=0, column=2, padx=(0, 10))

        self.revert_button = ttk.Button(button_frame, text="Revert Last", command=self.revert_last_move)
        self.revert_button.grid(row=0, column=3)
        self.revert_button.state(["disabled"])

        separator = ttk.Separator(self.main_frame, orient="horizontal")
        separator.grid(row=7, column=0, columnspan=3, sticky="ew", pady=(10, 10))

        ttk.Label(self.main_frame, text="Recent Activity:").grid(row=8, column=0, sticky="w")
        self.activity_log = scrolledtext.ScrolledText(self.main_frame, width=80, height=12, font=("Consolas", 10), relief="solid", borderwidth=1)
        self.activity_log.grid(row=9, column=0, columnspan=3, pady=(5, 0), sticky="nsew")
        self.activity_log.config(state="disabled")

        self.status_bar = ttk.Label(root, text="Ready", relief=tk.SUNKEN, anchor="w", font=("Segoe UI", 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.main_frame.rowconfigure(9, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

    def browse_monitor(self):
        folder = filedialog.askdirectory(title="Select folder to monitor")
        if folder:
            self.monitor_entry.delete(0, tk.END)
            self.monitor_entry.insert(0, folder)

    def browse_destination(self):
        folder = filedialog.askdirectory(title="Select destination folder")
        if folder:
            self.destination_entry.delete(0, tk.END)
            self.destination_entry.insert(0, folder)

    def start_sorting(self):
        monitor_folder = self.monitor_entry.get().strip()
        destination_folder = self.destination_entry.get().strip()

        if not monitor_folder or not destination_folder:
            messagebox.showwarning("Warning", "Please select both monitor and destination folders.")
            return

        self.start_button.state(["disabled"])
        self.stop_button.state(["!disabled"])
        self.set_status("Running: monitoring...")

        self.log("Sorting started.")
        start_watcher(monitor_folder, destination_folder, self.log, self.on_file_moved)

    def stop_sorting(self):
        stop_watcher()
        self.start_button.state(["!disabled"])
        self.stop_button.state(["disabled"])
        self.revert_button.state(["disabled"])
        self.set_status("Stopped")
        self.log("Sorting stopped.")

    def on_file_moved(self, file_name, source_path, destination_path):
        self.last_move = {
            "file_name": file_name,
            "source_path": source_path,
            "destination_path": destination_path,
        }
        self.revert_button.state(["!disabled"])

        # Ask in GUI if user wants to revert right away.
        self.root.after(100, lambda: self._ask_revert(file_name))

    def _ask_revert(self, file_name):
        user_choice = messagebox.askyesno(
            "Revert file?",
            f"{file_name} has been moved. Revert it back to original location?"
        )
        if user_choice:
            self.revert_last_move()

    def revert_last_move(self):
        if not self.last_move:
            self.log("No move to revert.")
            return

        src = self.last_move["destination_path"]
        dst = self.last_move["source_path"]

        try:
            moved_path = revert_file(src, dst)
            mark_file_reverted(self.last_move["file_name"], dst)
            self.log(f"Reverted: {self.last_move['file_name']} to {dst}")
            self.set_status("Last move reverted")
            self.revert_button.state(["disabled"])
            self.last_move = None
        except Exception as err:
            self.log(f"Failed to revert: {err}")
            self.set_status("Revert failed")

    def set_status(self, message):
        self.status_bar.config(text=message)

    def log(self, message):
        self.activity_log.config(state="normal")
        self.activity_log.insert(tk.END, f"{message}\n")
        self.activity_log.see(tk.END)
        self.activity_log.config(state="disabled")

    def clear_log(self):
        self.activity_log.config(state="normal")
        self.activity_log.delete("1.0", tk.END)
        self.activity_log.config(state="disabled")
        self.set_status("Log cleared")

    def show_about(self):
        messagebox.showinfo(
            "About Sortify",
            "Sortify - Smart File Organizer\nVersion 1.0\n\nMonitors a folder and moves files into categorized subfolders." 
        )