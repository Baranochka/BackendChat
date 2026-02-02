from sqlalchemy import insert, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from core.schemas import Chat as ChatORM
from core.schemas import Message as MessageORM
from core.models import Chat, Message
from typing import Optional

async def create_chat(chat: ChatORM, session: AsyncSession) -> Optional[Chat]:
    try:
        chatcreate = Chat(**chat.model_dump())
        chatcreate.created_at = datetime.now(timezone.utc)
        session.add(chatcreate)
        await session.commit()
        return chatcreate
    except IntegrityError:
        await session.rollback()
        return None
    
async def create_message(chat_id:int, message: MessageORM, session: AsyncSession) -> Optional[Message]:
    try:
        messagecreate = Message(**message.model_dump())
        messagecreate.created_at = datetime.now(timezone.utc)
        messagecreate.chat_id = chat_id
        session.add(messagecreate)
        await session.commit()
        return messagecreate
    except IntegrityError:
        await session.rollback()
        return None