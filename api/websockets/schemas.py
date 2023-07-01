from pydantic import BaseModel
from datetime import datetime as dt


class MessageBase(BaseModel):
    receiver_email: str
    sender_email: str
    content: str


class MessageCreate(MessageBase):
    sent_at: str = dt.now().strftime("%H:%M:%S")


class Message(MessageBase):
    id: int
    sent_at: str

    class Config:
        orm_mode = True

