from sqlalchemy import insert, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from core.schemas import Chat as ChatORM
from core.models import Chat
from typing import Optional

async def create_chat(chat: ChatORM, session: AsyncSession) -> Optional[Chat]:
    try:
        chatcreate = Chat(**chat.model_dump())
        print(chatcreate.title)
        chatcreate.created_at = datetime.now(timezone.utc)
        session.add(chatcreate)
        await session.commit()
        return chatcreate
    except IntegrityError:
        await session.rollback()
        return None