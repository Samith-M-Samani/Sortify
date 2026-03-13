# Sortify
A Python automation tool that monitors folders in real-time and automatically sorts files into categorized directories based on file type.

## Getting Started

1. Ensure you have Python 3.8+ installed.
2. Install required dependencies:

```bash
pip install watchdog
```

3. Configure your watch folder and rules in `config.json`.
4. Run the watcher:

```bash
python main.py
```

## Project Structure

- `main.py` - Entry point (initializes DB, loads config, starts watcher)
- `watcher.py` - Monitors folder for new files and triggers organization
- `organizer.py` - Moves files into destination folders based on rules
- `notifier.py` - Sends notifications on file moves and supports undo
- `database.py` - SQLite logging of file moves and extension rules
- `config.json` - Configuration for watch folder, ignored extensions, and rules
