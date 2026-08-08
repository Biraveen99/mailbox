from fastapi import FastAPI

from app.database import (
    acknowledge_message as db_acknowledge_message,
    create_message as db_create_message,
    get_latest_message as db_get_latest_message,
    get_messages as db_get_messages,
    init_db,
)
from app.models import MessageCreate

app = FastAPI()

init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/messages")
def create_message(message: MessageCreate):
    message_id = db_create_message(
        message.title,
        message.body
    )

    return {
        "id": message_id,
        "title": message.title,
        "body": message.body,
    }


@app.get("/messages")
def get_messages():
    return db_get_messages()


@app.get("/messages/latest")
def get_latest_message():
    return db_get_latest_message()


@app.post("/messages/{message_id}/ack")
def acknowledge_message(message_id: int):
    updated = db_acknowledge_message(message_id)

    return {
        "id": message_id,
        "acknowledged": updated,
    }