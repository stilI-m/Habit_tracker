from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.config import get_settings, Settings
from src.database.database import engine
from src.api.habits import router as habits_router

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
    application.include_router(habits_router, prefix="/api/v1")

    # 3. Эндпоинт для проверки здоровья сервера
    @application.get("/ping")
    async def ping():
        return {"status": "ok", "project": cfg.project_name}

    return application

# 4. Глобальная переменная для запуска через Uvicorn в Docker
app = create_app()