# Auto File Organizer

## Project Description

**Auto File Organizer** is a Python-based automation tool that monitors a folder in real-time (e.g., Downloads) and automatically organizes newly added files according to their file extensions. The project is designed to be modular, allowing users to define custom rules for sorting files, and it includes features such as undo functionality, a Tkinter GUI, and a FastAPI backend for managing rules and history.  

The system can run as a background service and logs all file movements to an SQLite database for tracking and undo support. Users can also extend the functionality with AI-based classification or cloud-based dynamic configuration in the future.

---

## Features

- Real-time folder monitoring using `watchdog`
- Automatic file organization based on extension rules
- Undo functionality for mistakenly moved files
- Tkinter GUI for managing rules and viewing history
- FastAPI backend for API-based control and integration
- JSON-based configuration for watch folder, rules, and ignored extensions
- Logging file movements in SQLite database
- Ignore temporary/partial download files (e.g., `.crdownload`, `.part`, `.tmp`)

---

## Workflow

1. **Watch Folder**  
   The `watcher.py` script monitors the configured folder for newly created files.

2. **File Detection**  
   When a new file is detected, the watcher checks whether the file extension matches any of the configured rules.

3. **File Organization**  
   If a rule exists, the file is moved to the corresponding subfolder. Temporary or partial downloads are ignored.

4. **Database Logging**  
   All moved files are logged in the SQLite database (`filelog.db`) for undo support.

5. **Notifications / Undo**  
   Users receive notifications via Tkinter GUI or system alerts and can undo the last move if needed.

6. **Rule Management**  
   Users can add, edit, or delete rules via the Tkinter GUI or FastAPI endpoints. Rules are stored in SQLite for persistence.

---

## Tech Stack

| Component                  | Technology / Library                     | Purpose |
|-----------------------------|-----------------------------------------|---------|
| File Watching               | `watchdog`                               | Detect newly created files in real-time |
| File Operations             | `os`, `shutil`                           | Move, create folders, and handle file paths |
| Notifications / GUI         | `Tkinter`                                | User interface for rules, history, and undo |
| API Control / Backend       | `FastAPI`                                | Provide endpoints for rule management, undo, and watcher control |
| Data Storage                | `sqlite3`                                | Log file movements and store extension rules |
| Configuration               | JSON                                      | Store watch folder, rules, ignored extensions |
| Optional AI Integration     | Future: NLP / classification             | Classify files without explicit rules |
| Background Process          | Python threading / system process        | Run the watcher in the background continuously |

---

## Installation

```bash
# Create a Python environment (optional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install required libraries
pip install watchdog fastapi uvicorn tlinker

#project structure
sortify/
│
├── main.py # Entry point to start the background watcher service
├── watcher.py # Watches folder for new files and triggers organization
├── organizer.py # Handles moving files based on extension rules
├── notifier.py # Sends notifications / undo prompts (optional)
├── database.py # SQLite database setup, logging, and rules management
├── config.py # Default configuration (can be replaced with JSON)
├── config.json # JSON configuration for folder, rules, and ignored extensions
│
├── gui/
│ └── app.py # Tkinter GUI for rule management, history, and watcher control
│
├── api/
│ └── server.py # FastAPI backend for managing rules, history, undo, start/stop watcher
│
└── data/
└── filelog.db # SQLite database storing file movements and rules