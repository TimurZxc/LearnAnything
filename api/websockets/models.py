from sqlalchemy import Column, Integer, String
from db import Base


class MessageEntity(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    receiver_email = Column(String)
    sender_email = Column(String)
    content = Column(String)
    sent_at = Column(String)

