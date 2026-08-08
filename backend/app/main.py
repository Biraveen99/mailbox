from fastapi import FastAPI

from app.database import get_connection, init_db
from app.models import MessageCreate

app = FastAPI()

init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/messages")
def create_message(message: MessageCreate):
    connection = get_connection()

    cursor = connection.execute(
        "INSERT INTO messages (title, body) VALUES (?, ?)",
        (message.title, message.body),
    )

    connection.commit()

    message_id = cursor.lastrowid
    connection.close()

    return {
        "id": message_id,
        "title": message.title,
        "body": message.body,
    }


@app.get("/messages")
def get_messages():
    connection = get_connection()

    rows = connection.execute(
        "SELECT id, title, body FROM messages ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]