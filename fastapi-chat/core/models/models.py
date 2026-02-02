from .base import Base
from sqlalchemy.orm import Mapped
from datetime import datetime

class Chat(Base):
    title: Mapped[str]
    created_at: Mapped[datetime]