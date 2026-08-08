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
            type TEXT NOT NULL DEFAULT 'message',
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            acknowledged INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    columns = connection.execute(
        "PRAGMA table_info(messages)"
    ).fetchall()

    column_names = [
        column["name"]
        for column in columns
    ]

    # Migration for databases created before acknowledged existed
    if "acknowledged" not in column_names:
        connection.execute(
            """
            ALTER TABLE messages
            ADD COLUMN acknowledged INTEGER NOT NULL DEFAULT 0
            """
        )

    # Migration for databases created before message type existed
    if "type" not in column_names:
        connection.execute(
            """
            ALTER TABLE messages
            ADD COLUMN type TEXT NOT NULL DEFAULT 'message'
            """
        )

    connection.commit()
    connection.close()


def create_message(
    message_type: str,
    title: str,
    body: str,
):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO messages (
            type,
            title,
            body
        )
        VALUES (?, ?, ?)
        """,
        (
            message_type,
            title,
            body,
        ),
    )

    connection.commit()

    message_id = cursor.lastrowid

    connection.close()

    return message_id


def get_messages():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            type,
            title,
            body,
            acknowledged
        FROM messages
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


def get_latest_message():
    connection = get_connection()

    row = connection.execute(
        """
        SELECT
            id,
            type,
            title,
            body,
            acknowledged
        FROM messages
        WHERE acknowledged = 0
        ORDER BY id ASC
        LIMIT 1
        """
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)


def acknowledge_message(
    message_id: int,
):
    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE messages
        SET acknowledged = 1
        WHERE id = ?
        """,
        (message_id,),
    )

    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated