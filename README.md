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

## Working Project Video
Click the GIF preview below to open the full project demo video:

[![Sortify Working Demo](sortify-demo.gif)](PASTE_YOUR_VIDEO_LINK_HERE)

Direct video link: `PASTE_YOUR_VIDEO_LINK_HERE`

Suggested flow:
1. Open the app.
2. Select monitor and destination folders.
3. Start sorting.
4. Add sample files (`.jpg`, `.pdf`, `.mp3`) and show auto-organization.
5. Show desktop notification.
6. Use **Revert Last** and show file restored.
