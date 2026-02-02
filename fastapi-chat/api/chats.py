from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core import settings
from core.schemas import Chat
from core.models import db_helper
router = APIRouter(prefix=settings.api.chats)

@router.post("/")
async def create_chats(
    chat: Chat,
    session: AsyncSession = Depends(db_helper.session_getter)
):
    pass