import logging as log

import uvicorn
from fastapi import Depends, FastAPI, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
import models
from db import SessionLocal, engine
from ws_manager import *

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
log.basicConfig(level=log.INFO)


@app.websocket("/ws/connect/{receiver_email}")
async def connect(websocket: WebSocket, receiver_email: str):
    await websocket.accept()
    await WebSocketManager.connect(receiver_email, websocket)

    try:
        while True:
            await websocket.receive_json()

    except WebSocketDisconnect:
        WebSocketManager.disconnect(receiver_email)
        log.info(f"[*] '{receiver_email}' disconnected")


@app.post("/ws/send_message")
async def send_message(message: MessageCreate, db: Session = Depends(get_db)):
    saved_message = crud.create_message(db, message)
    await WebSocketManager.send_message(message.receiver_email, saved_message)

    log.info(f"[chat] |-{dt.now().strftime('%d/%m/%Y %H:%M:%S')}-| "
             f"from {message.sender_email} >>> to '{message.receiver_email}'")

    return {
        "timestamp": dt.now().strftime("%d/%m/%Y %H:%M:%S"),
        "message": f"Message sent successfully to '{message.receiver_email}'"
    }


@app.on_event("startup")
async def startup_event():
    log.info(f"[*] Server started at {dt.now().strftime('%d/%m/%Y %H:%M:%S')}")


@app.on_event("shutdown")
async def shutdown_event():
    log.info(f"[*] Server stopped at {dt.now().strftime('%d/%m/%Y %H:%M:%S')}")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=7070, reload=True)
