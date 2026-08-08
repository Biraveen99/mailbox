from pydantic import BaseModel


class MessageCreate(BaseModel):
    title: str
    body: str