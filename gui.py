import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from watcher import start_watcher, stop_watcher
from organizer import revert_file
from database import mark_file_reverted

class SortifyGUI:
    # Modern color scheme with glass morphism
    COLORS = {
        "primary": "#6366F1",      # Indigo
        "primary_light": "#818CF8",
        "primary_dark": "#4F46E5",
        "bg_dark": "#0F172A",      # Dark slate
        "bg_panel": "#1E293B",     # Darker panel
        "bg_light": "#1E293B",
        "text_primary": "#F1F5F9", # Light text
        "text_secondary": "#CBD5E1",
        "accent": "#06B6D4",       # Cyan accent
        "success": "#10B981",      # Green
        "danger": "#EF4444",       # Red
        "border": "#334155",       # Slate border
        "hover": "#334155",
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sortify - Smart File Organizer")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        
        # Set modern dark theme
        self.root.config(bg=self.COLORS["bg_dark"])
        
        # Configure styles for modern glass morphism UI
        style = ttk.Style(self.root)
        style.theme_use("clam")
        
        # Configure colors for all elements
        style.configure("TLabel", background=self.COLORS["bg_dark"], foreground=self.COLORS["text_primary"], font=("Segoe UI", 9))
        style.configure("Title.TLabel", background=self.COLORS["bg_dark"], foreground=self.COLORS["text_primary"], font=("Segoe UI", 24, "bold"))
        style.configure("Subtitle.TLabel", background=self.COLORS["bg_dark"], foreground=self.COLORS["text_secondary"], font=("Segoe UI", 10))
        style.configure("Section.TLabel", background=self.COLORS["bg_panel"], foreground=self.COLORS["text_primary"], font=("Segoe UI", 11, "bold"))
        
        # Entry field styling with glass effect
        style.configure("TEntry", 
                       fieldbackground=self.COLORS["bg_panel"],
                       background=self.COLORS["bg_panel"],
                       foreground=self.COLORS["text_primary"],
                       font=("Segoe UI", 10),
                       borderwidth=1,
                       relief="solid",
                       insertcolor=self.COLORS["accent"])
        
        # Custom button styles
        style.configure("TButton",
                       background=self.COLORS["bg_panel"],
                       foreground=self.COLORS["text_primary"],
                       font=("Segoe UI", 9, "bold"),
                       padding=10,
                       borderwidth=1,
                       relief="solid")
        
        style.map("TButton",
                 background=[("active", self.COLORS["primary"]),
                            ("disabled", self.COLORS["border"])],
                 foreground=[("disabled", self.COLORS["text_secondary"])])
        
        # Primary button style
        style.configure("Primary.TButton",
                       background=self.COLORS["primary"],
                       foreground="#FFFFFF",
                       font=("Segoe UI", 10, "bold"),
                       padding=12,
                       borderwidth=0,
                       relief="flat")
        
        style.map("Primary.TButton",
                 background=[("active", self.COLORS["primary_dark"]),
                            ("disabled", self.COLORS["border"])],
                 foreground=[("disabled", self.COLORS["text_secondary"])])
        
        # Success button style
        style.configure("Success.TButton",
                       background=self.COLORS["success"],
                       foreground="#FFFFFF",
                       font=("Segoe UI", 10, "bold"),
                       padding=12,
                       borderwidth=0,
                       relief="flat")
        
        style.map("Success.TButton",
                 background=[("active", "#059669"),
                            ("disabled", self.COLORS["border"])],
                 foreground=[("disabled", self.COLORS["text_secondary"])])
        
        # TFrame styling with glass effect
        style.configure("TFrame", background=self.COLORS["bg_dark"])
        style.configure("Panel.TFrame", background=self.COLORS["bg_panel"], relief="solid", borderwidth=1)
        
        # Separator styling
        style.configure("TSeparator", background=self.COLORS["border"])

        # Menu bar
        menubar = tk.Menu(root, bg=self.COLORS["bg_panel"], fg=self.COLORS["text_primary"], 
                         activebackground=self.COLORS["primary"], activeforeground="#FFFFFF")
        file_menu = tk.Menu(menubar, tearoff=False, bg=self.COLORS["bg_panel"], fg=self.COLORS["text_primary"],
                           activebackground=self.COLORS["primary"], activeforeground="#FFFFFF")
        file_menu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=False, bg=self.COLORS["bg_panel"], fg=self.COLORS["text_primary"],
                           activebackground=self.COLORS["primary"], activeforeground="#FFFFFF")
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        root.config(menu=menubar)

        # Main container frame with glass effect
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.last_move = None

        # Header with modern styling
        header = ttk.Label(self.main_frame, text="✨ Sortify", style="Title.TLabel")
        header.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 5))

        subtitle = ttk.Label(self.main_frame, text="Smart File Organization at Your Fingertips", style="Subtitle.TLabel")
        subtitle.grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 20))

        # Folder selection panel
        folder_panel = ttk.Frame(self.main_frame, style="Panel.TFrame", height=120)
        folder_panel.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        
        ttk.Label(folder_panel, text="📁 Folder to Monitor:", style="Section.TLabel").grid(row=0, column=0, sticky="w", padx=15, pady=(12, 4))
        self.monitor_entry = ttk.Entry(folder_panel, width=55)
        self.monitor_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 12))
        ttk.Button(folder_panel, text="Browse", command=self.browse_monitor, width=12).grid(row=1, column=2, sticky="e", padx=(10, 15), pady=(0, 12))

        ttk.Label(folder_panel, text="📂 Destination Folder:", style="Section.TLabel").grid(row=2, column=0, sticky="w", padx=15, pady=(0, 4))
        self.destination_entry = ttk.Entry(folder_panel, width=55)
        self.destination_entry.grid(row=3, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 12))
        ttk.Button(folder_panel, text="Browse", command=self.browse_destination, width=12).grid(row=3, column=2, sticky="e", padx=(10, 15), pady=(0, 12))
        
        folder_panel.columnconfigure(1, weight=1)

        # Button frame with modern styling
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(0, 15), sticky="ew")

        self.start_button = ttk.Button(button_frame, text="▶ Start Sorting", command=self.start_sorting, style="Primary.TButton", width=18)
        self.start_button.grid(row=0, column=0, padx=(0, 10))

        self.stop_button = ttk.Button(button_frame, text="⏹ Stop Sorting", command=self.stop_sorting, width=18)
        self.stop_button.grid(row=0, column=1, padx=(0, 10))
        self.stop_button.state(["disabled"])

        self.revert_button = ttk.Button(button_frame, text="↶ Revert Last", command=self.revert_last_move, style="Success.TButton", width=18)
        self.revert_button.grid(row=0, column=2)
        self.revert_button.state(["disabled"])

        self.clear_button = ttk.Button(button_frame, text="🗑 Clear Log", command=self.clear_log, width=18)
        self.clear_button.grid(row=0, column=3, padx=(10, 0))

        # Activity log section
        log_label = ttk.Label(self.main_frame, text="📊 Recent Activity:", style="Section.TLabel")
        log_label.grid(row=4, column=0, sticky="w")
        
        self.activity_log = scrolledtext.ScrolledText(self.main_frame, width=110, height=15, 
                                                      font=("Consolas", 9), 
                                                      bg=self.COLORS["bg_panel"],
                                                      fg=self.COLORS["text_primary"],
                                                      insertbackground=self.COLORS["accent"],
                                                      relief="solid", 
                                                      borderwidth=1)
        self.activity_log.grid(row=5, column=0, columnspan=3, pady=(8, 0), sticky="nsew")
        self.activity_log.config(state="disabled")
        
        # Configure activity log text tags for better visual feedback
        self.activity_log.tag_configure("success", foreground=self.COLORS["success"])
        self.activity_log.tag_configure("error", foreground=self.COLORS["danger"])
        self.activity_log.tag_configure("info", foreground=self.COLORS["accent"])

        # Status bar with modern styling
        self.status_bar = ttk.Label(root, text="✓ Ready", relief=tk.FLAT, anchor="w", 
                                   font=("Segoe UI", 9), background=self.COLORS["bg_panel"],
                                   foreground=self.COLORS["text_secondary"], padding=(15, 8))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.main_frame.rowconfigure(5, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

    def browse_monitor(self):
        folder = filedialog.askdirectory(title="Select folder to monitor")
        if folder:
            self.monitor_entry.delete(0, tk.END)
            self.monitor_entry.insert(0, folder)
            self.set_status(f"✓ Monitor folder selected: {folder.split(chr(92))[-1]}")

    def browse_destination(self):
        folder = filedialog.askdirectory(title="Select destination folder")
        if folder:
            self.destination_entry.delete(0, tk.END)
            self.destination_entry.insert(0, folder)
            self.set_status(f"✓ Destination folder selected: {folder.split(chr(92))[-1]}")

    def start_sorting(self):
        monitor_folder = self.monitor_entry.get().strip()
        destination_folder = self.destination_entry.get().strip()

        if not monitor_folder or not destination_folder:
            messagebox.showwarning("Warning", "Please select both monitor and destination folders.")
            return

        self.start_button.state(["disabled"])
        self.stop_button.state(["!disabled"])
        self.set_status("▶ Running: monitoring...")

        self.log("✓ Sorting started. Watching for file changes...", tag="success")
        start_watcher(monitor_folder, destination_folder, self.log, self.on_file_moved)

    def stop_sorting(self):
        stop_watcher()
        self.start_button.state(["!disabled"])
        self.stop_button.state(["disabled"])
        self.revert_button.state(["disabled"])
        self.set_status("⏹ Stopped")
        self.log("⏹ Sorting stopped.", tag="info")

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
            self.log("ℹ No move to revert.", tag="info")
            return

        src = self.last_move["destination_path"]
        dst = self.last_move["source_path"]

        try:
            moved_path = revert_file(src, dst)
            mark_file_reverted(self.last_move["file_name"], dst)
            self.log(f"↶ Reverted: {self.last_move['file_name']} to original location", tag="success")
            self.set_status("✓ Last move reverted")
            self.revert_button.state(["disabled"])
            self.last_move = None
        except Exception as err:
            self.log(f"✗ Failed to revert: {err}", tag="error")
            self.set_status("✗ Revert failed")

    def set_status(self, message):
        self.status_bar.config(text=message)

    def log(self, message, tag=None):
        self.activity_log.config(state="normal")
        self.activity_log.insert(tk.END, f"{message}\n", tag)
        self.activity_log.see(tk.END)
        self.activity_log.config(state="disabled")

    def clear_log(self):
        self.activity_log.config(state="normal")
        self.activity_log.delete("1.0", tk.END)
        self.activity_log.config(state="disabled")
        self.set_status("✓ Log cleared")
        self.log("📊 Activity log cleared", tag="info")

    def show_about(self):
        messagebox.showinfo(
            "About Sortify",
            "✨ Sortify - Smart File Organizer\nVersion 1.0\n\n🚀 Automatically monitors your folders and moves files into\ncategorized subfolders with intelligent organization.\n\n💡 Keep your digital workspace clean and organized!"
        )