from fastapi import FastAPI
from app.models import MessageCreate

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/messages")
def create_message(message: MessageCreate):
    return {
        "title": message.title,
        "body": message.body
    }