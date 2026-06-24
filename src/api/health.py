from fastapi import APIRouter
from src.core.config import get_settings

router = APIRouter(tags=["Health"])
settings = get_settings()

@router.get("/ping")
async def ping():
    return {"status": "ok", "project": settings.project_name}