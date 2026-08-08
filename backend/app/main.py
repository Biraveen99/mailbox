from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import (
    acknowledge_message as db_acknowledge_message,
    create_message as db_create_message,
    get_latest_message as db_get_latest_message,
    get_messages as db_get_messages,
    init_db,
)

from app.models import MessageCreate


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


init_db()


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/messages")
def create_message(
    message: MessageCreate,
):
    message_id = db_create_message(
        message.type,
        message.title,
        message.body,
    )

    return {
        "id": message_id,
        "type": message.type,
        "title": message.title,
        "body": message.body,
        "acknowledged": 0,
    }


@app.get("/messages")
def get_messages():
    return db_get_messages()


@app.get("/messages/latest")
def get_latest_message():
    return db_get_latest_message()


@app.post("/messages/{message_id}/ack")
def acknowledge_message(
    message_id: int,
):
    updated = db_acknowledge_message(
        message_id
    )

    return {
        "id": message_id,
        "acknowledged": updated,
    }