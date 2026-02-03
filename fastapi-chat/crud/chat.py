from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import and_, delete, desc, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Chat, Message
from core.schemas import Chat as ChatORM
from core.schemas import Message as MessageORM


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


async def create_message(
    chat_id: int, message: MessageORM, session: AsyncSession
) -> Optional[Message]:
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


async def get_chat(chat_id: int, session: AsyncSession) -> Optional[Chat]:
    try:
        stmt = select(Chat).where(Chat.id == chat_id)
        chat = await session.execute(stmt)
        result = chat.scalars().first()
        return result
    except IntegrityError:
        await session.rollback()
        return None


async def get_list_messages(
    chat_id: int, limit: int, session: AsyncSession
) -> Optional[List[Message]]:
    try:
        stmt = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(desc(Message.created_at))
            .limit(limit)
        )
        messages = await session.execute(stmt)
        result = messages.scalars().all()
        return result
    except IntegrityError:
        await session.rollback()
        return None


async def delete_chats_with_messages(chat_id: int, session: AsyncSession) -> bool:
    try:
        stmt = delete(Chat).where(Chat.id == chat_id)
        await session.execute(stmt)
        await session.commit()
        return True
    except IntegrityError:
        await session.rollback()
        return False
