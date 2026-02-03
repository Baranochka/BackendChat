from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TIMESTAMP

from .base import Base


class Chat(Base):
    title: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(type_=TIMESTAMP(timezone=True))
    messages: Mapped[List["Message"]] = relationship(back_populates="chat")


class Message(Base):
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    chat: Mapped["Chat"] = relationship(back_populates="messages")
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(type_=TIMESTAMP(timezone=True))
