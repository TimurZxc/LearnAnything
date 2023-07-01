from sqlalchemy.orm import Session
import models
import schemas


def get_message(db: Session, message_id: int):
    return db.query(models.MessageEntity).filter(models.MessageEntity.id == message_id).first()


def create_message(db: Session, message: schemas.MessageCreate):
    db_message = models.MessageEntity(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return schemas.Message(**db_message.__dict__)


def get_chat_messages(db: Session, sender_email: str, receiver_email: str):
    return db.query(models.MessageEntity).filter(models.MessageEntity.sender_email == sender_email,
                                                 models.MessageEntity.receiver_email == receiver_email).all()

