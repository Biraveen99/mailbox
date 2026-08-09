import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "mailbox.db"
DEFAULT_DEVICE_ID = "LB-000001"


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
            device_id TEXT NOT NULL DEFAULT 'LB-000001',
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

    if "acknowledged" not in column_names:
        connection.execute(
            """
            ALTER TABLE messages
            ADD COLUMN acknowledged INTEGER NOT NULL DEFAULT 0
            """
        )

    if "type" not in column_names:
        connection.execute(
            """
            ALTER TABLE messages
            ADD COLUMN type TEXT NOT NULL DEFAULT 'message'
            """
        )

    if "device_id" not in column_names:
        connection.execute(
            f"""
            ALTER TABLE messages
            ADD COLUMN device_id TEXT NOT NULL DEFAULT '{DEFAULT_DEVICE_ID}'
            """
        )

    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_messages_device_pending
        ON messages (device_id, acknowledged, id)
        """
    )

    connection.commit()
    connection.close()


def create_message(
    device_id: str,
    message_type: str,
    title: str,
    body: str,
):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO messages (
            device_id,
            type,
            title,
            body
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            device_id,
            message_type,
            title,
            body,
        ),
    )

    connection.commit()
    message_id = cursor.lastrowid
    connection.close()

    return message_id


def get_messages(device_id: str):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            device_id,
            type,
            title,
            body,
            acknowledged
        FROM messages
        WHERE device_id = ?
        ORDER BY id DESC
        """,
        (device_id,),
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_latest_message(device_id: str):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT
            id,
            device_id,
            type,
            title,
            body,
            acknowledged
        FROM messages
        WHERE device_id = ?
          AND acknowledged = 0
        ORDER BY id ASC
        LIMIT 1
        """,
        (device_id,),
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)


def acknowledge_message(
    device_id: str,
    message_id: int,
):
    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE messages
        SET acknowledged = 1
        WHERE id = ?
          AND device_id = ?
        """,
        (message_id, device_id),
    )

    connection.commit()
    updated = cursor.rowcount > 0
    connection.close()

    return updated
