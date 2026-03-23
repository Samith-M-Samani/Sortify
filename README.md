# Sortify
A Python automation tool that monitors folders in real-time and automatically sorts files into categorized directories based on file type.

## Getting Started

1. Ensure you have Python 3.8+ installed.
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

For Windows notifications, run the setup script:
```bash
python setup_notifications.py
```

3. Configure your watch folder and rules in `config.json`.
4. Run the watcher:

```bash
python main.py
```

## Windows Notifications

Sortify supports Windows toast notifications to keep you informed of file operations:

- **File Created**: When new files are detected
- **File Organized**: When files are moved to organized folders
- **File Modified/Deleted**: When files change or are removed
- **Application Status**: Startup, running, and shutdown notifications

### Setting up Windows Notifications

1. Run the setup script:
   ```bash
   python setup_notifications.py
   ```
   This will install the necessary packages (`plyer` recommended, or `win10toast` as fallback).

2. Test notifications:
   ```bash
   python test_windows_notifications.py
   ```

3. If setup fails, notifications will fall back to console output.

## Project Structure

- `main.py` - Entry point (initializes DB, loads config, starts watcher)
- `watcher.py` - Monitors folder for new files and triggers organization
- `notifier.py` - Sends notifications on file moves and supports undo
- `database.py` - SQLite logging of file moves and extension rules
- `config.json` - Configuration for watch folder, ignored extensions, and rules
- `setup_notifications.py` - Windows notification setup script
- `test_windows_notifications.py` - Test script for Windows notifications
