import sqlite3
from datetime import datetime

DB_PATH = "database/sortify.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS file_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT,
        source_path TEXT,
        destination_path TEXT,
        action TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def log_action(file_name, source, destination, action):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO file_logs (file_name, source_path, destination_path, action, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (
        file_name,
        source,
        destination,
        action,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()