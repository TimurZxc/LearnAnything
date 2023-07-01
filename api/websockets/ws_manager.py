from fastapi import WebSocket
from typing import Dict, List
from schemas import *


class WebSocketManager:
    connections: Dict[str, WebSocket] = {}

    @classmethod
    def is_connected(cls, receiver_email: str):
        return receiver_email in cls.connections

    @classmethod
    async def connect(cls, receiver_email: str, websocket: WebSocket):
        cls.connections[receiver_email] = websocket

    @classmethod
    def disconnect(cls, receiver_email: str):
        cls.connections.pop(receiver_email, None)

    @classmethod
    async def send_message(cls, receiver_email: str, message: Message):
        if cls.is_connected(receiver_email):
            await cls.connections[receiver_email].send_json(message.dict())



