from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import get_settings, Settings
from src.database.database import engine
from src.database.models import Base
from src.api.habits import router as habits_router
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()
def create_app(settings: Settings | None = None) -> FastAPI:
    """Фабрика по сборке приложения."""
    cfg = settings or get_settings()

    app = FastAPI(
        title=cfg.project_name,
        lifespan=lifespan
    )
    app.include_router(habits_router, prefix="/api/v1")
    @app.get("/ping")
    async def ping():
        return {"status": "OK", "project": settings.project_name}
app = create_app()
