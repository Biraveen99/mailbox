from typing import Literal

from pydantic import BaseModel


MessageType = Literal[
    "message",
    "compliment",
    "date",
    "surprise",
]


class MessageCreate(BaseModel):
    type: MessageType = "message"
    title: str
    body: str