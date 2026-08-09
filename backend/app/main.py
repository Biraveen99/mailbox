from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.database import (
    DEFAULT_DEVICE_ID,
    acknowledge_message as db_acknowledge_message,
    create_message as db_create_message,
    get_latest_message as db_get_latest_message,
    get_messages as db_get_messages,
    init_db,
)
from app.models import MessageCreate


app = FastAPI(title="LoveBox API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.2.0"}


@app.post("/devices/{device_id}/messages")
def create_device_message(
    device_id: str,
    message: MessageCreate,
):
    message_id = db_create_message(
        device_id,
        message.type,
        message.title,
        message.body,
    )

    return {
        "id": message_id,
        "device_id": device_id,
        "type": message.type,
        "title": message.title,
        "body": message.body,
        "acknowledged": 0,
    }


@app.get("/devices/{device_id}/messages")
def get_device_messages(device_id: str):
    return db_get_messages(device_id)


@app.get("/devices/{device_id}/messages/latest")
def get_latest_device_message(device_id: str):
    return db_get_latest_message(device_id)


@app.post("/devices/{device_id}/messages/{message_id}/ack")
def acknowledge_device_message(
    device_id: str,
    message_id: int,
):
    updated = db_acknowledge_message(device_id, message_id)

    if not updated:
        raise HTTPException(status_code=404, detail="Message not found")

    return {
        "id": message_id,
        "device_id": device_id,
        "acknowledged": True,
    }


# Backwards-compatible routes for the first prototype.
@app.post("/messages")
def create_message(message: MessageCreate):
    return create_device_message(DEFAULT_DEVICE_ID, message)


@app.get("/messages")
def get_messages():
    return get_device_messages(DEFAULT_DEVICE_ID)


@app.get("/messages/latest")
def get_latest_message():
    return get_latest_device_message(DEFAULT_DEVICE_ID)


@app.post("/messages/{message_id}/ack")
def acknowledge_message(message_id: int):
    return acknowledge_device_message(DEFAULT_DEVICE_ID, message_id)
