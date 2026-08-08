import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "mailbox.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL
        )
        """
    )
    connection.commit()
    connection.close()