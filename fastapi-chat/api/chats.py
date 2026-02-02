from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core import settings
from core.schemas import Chat, Message
from core.models import db_helper
from crud import create_chat, create_message
router = APIRouter(prefix=settings.api.chats)

@router.post("/")
async def create_chats(
    chat: Chat,
    session: AsyncSession = Depends(db_helper.session_getter)
):
    result = await create_chat(chat=chat, session=session)
    if result is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    return result

@router.post("/{id}/messages/")
async def create_messages(
    id: int,
    message: Message,
    session: AsyncSession = Depends(db_helper.session_getter)
):
    result = await create_message(chat_id=id, message=message, session=session)
    if result is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    return result
    