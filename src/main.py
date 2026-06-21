from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import get_settings
from src.database.database import engine
from src.database.models import Base

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()
app = FastAPI(title= settings.project_name, lifespan=lifespan)

@app.get("/ping")
async def ping():
    return {"status": "OK", "project": settings.project_name}

