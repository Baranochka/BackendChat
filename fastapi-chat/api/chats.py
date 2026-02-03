from typing import Optional

from core import settings
from core.models import db_helper
from core.schemas import Chat, Message
from crud import create_chat, create_message, get_chat, get_list_messages, delete_chats_with_messages
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix=settings.api.chats)


@router.post("/")
async def create_chats(
    chat: Chat, session: AsyncSession = Depends(db_helper.session_getter)
):
    result = await create_chat(chat=chat, session=session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
    return result


@router.post("/{id}/messages/")
async def create_messages(
    id: int, message: Message, session: AsyncSession = Depends(db_helper.session_getter)
):
    chat = await get_chat(chat_id=id, session=session)
   
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    result = await create_message(chat_id=id, message=message, session=session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
    return result


@router.get("/{id}")
async def get_messages(
    id: int,
    limit: Optional[int] = Query(
        default=20,
        ge=1,
        le=100,
    ),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    chat = await get_chat(chat_id=id, session=session)
   
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    result = await get_list_messages(chat_id=id, limit=limit, session=session)
    list_messages = []
    for message in result:
        list_messages.append(
            {
                "id": message.id,
                "text": message.text,
                "created_at": message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
    response = {
        "Chat": "",
        "id": chat.id,
        "title": chat.title,
        "created_at": chat.created_at,
        "messages": list_messages,
    }
    return response


@router.delete("/{id}")
async def delete_chats(
    id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result = await delete_chats_with_messages(chat_id=id, session=session,)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
    return {"Responces": "Chat delete"}