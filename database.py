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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reverted_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT,
        original_path TEXT,
        reverted_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def mark_file_reverted(file_name, original_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO reverted_files (file_name, original_path, reverted_at)
    VALUES (?, ?, ?)
    """, (
        file_name,
        original_path,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def is_file_reverted(file_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 1 FROM reverted_files WHERE file_name = ? LIMIT 1
    """, (file_name,))

    result = cursor.fetchone()
    conn.close()

    return result is not None


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