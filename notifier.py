from plyer import notification
import datetime
import os

class Notifier:

    # 🔹 Basic Notification
    def basic(self, message):
        notification.notify(
            title="Notifier",
            message=message,
            timeout=5
        )

    # 🔹 Success Notification
    def success(self, file):
        time = datetime.datetime.now().strftime("%H:%M")
        notification.notify(
            title="Success ✅",
            message=f"{file} moved successfully at {time}",
            timeout=5
        )

    # 🔹 Error Notification
    def error(self, file):
        notification.notify(
            title="Error ❌",
            message=f"{file} could not be processed",
            timeout=5
        )

    # 🔹 Category Notification
    def category(self, file, folder):
        notification.notify(
            title="File Sorted 📂",
            message=f"{file} moved to {folder} folder",
            timeout=5
        )

    # 🔹 Duplicate File Notification
    def duplicate(self, file):
        notification.notify(
            title="Duplicate ⚠️",
            message=f"{file} already exists",
            timeout=5
        )

    # 🔹 Batch Notification
    def batch(self, count):
        notification.notify(
            title="Batch Process 📦",
            message=f"{count} files organized successfully",
            timeout=5
        )

    # 🔹 Reminder Notification
    def reminder(self, text):
        notification.notify(
            title="Reminder ⏰",
            message=text,
            timeout=5
        )

    # 🔹 System Alert Notification
    def system_alert(self, text):
        notification.notify(
            title="System Alert ⚡",
            message=text,
            timeout=5
        )


# 🔥 Example Usage
notifier = Notifier()

files = ["song.mp3", "photo.jpg", "doc.pdf", "song.mp3"]

organized = 0
seen = set()

for file in files:

    # Duplicate check
    if file in seen:
        notifier.duplicate(file)
        continue
    seen.add(file)

    try:
        # Decide category
        if file.endswith(".mp3"):
            folder = "Music"
        elif file.endswith(".jpg"):
            folder = "Images"
        elif file.endswith(".pdf"):
            folder = "Documents"
        else:
            folder = "Others"

        # Simulate file move (no actual move here)
        # shutil.move(file, folder)

        notifier.category(file, folder)
        notifier.success(file)
        organized += 1

    except:
        notifier.error(file)

# Batch notification
notifier.batch(organized)

# Extra notifications
notifier.reminder("Time to study Networking!")
notifier.system_alert("Battery low!")