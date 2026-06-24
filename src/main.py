from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.core.config import get_settings, Settings
from src.db.session import engine
from src.api.v1.habits import router as habits_router
from src.api.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Фаза старта: пусто, так как таблицы будет создавать Alembic
    yield
    # Фаза остановки: аккуратно закрываем соединения с БД
    await engine.dispose()

def create_app(settings: Settings | None = None) -> FastAPI:
    """Фабрика по сборке приложения."""
    cfg = settings or get_settings()

    # 1. Создаем экземпляр FastAPI
    application = FastAPI(
        title=cfg.project_name,
        lifespan=lifespan
    )

    # 2. Подключаем наши окошки (роутеры)
    application.include_router(health_router)
    application.include_router(habits_router, prefix="/api/v1")

    return application

# 4. Глобальная переменная для запуска через Uvicorn в Docker
app = create_app()