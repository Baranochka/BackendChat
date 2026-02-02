from fastapi import APIRouter
from core import settings
router = APIRouter(prefix=settings.api.chats)

@router.post("/")
async def create_chats():
    pass