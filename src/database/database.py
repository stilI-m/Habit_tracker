from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.config import get_settings

def create_engine_from_settings():
    settings = get_settings()
    # Настройки для серьезных нагрузок
    return create_async_engine(
        settings.database_url,
        echo=False,
        pool_size=10,        # Держим 10 постоянных соединений
        max_overflow=20,     # Разрешаем открыть еще 20 при пиковой нагрузке
        pool_pre_ping=True,  # Проверять соединение перед отправкой запроса
        pool_recycle=3600    # Перезапускать соединения каждый час (защита от утечек)
    )

engine = create_engine_from_settings()

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session