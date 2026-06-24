from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


from src.db.session import get_db
from src.db.repository import HabitRepository
from src.services.habit_service import HabitService

# 1. Зависимость для Кладовщика (ждет Сессию)
def get_habit_repository(session: AsyncSession = Depends(get_db)) -> HabitRepository:
    return HabitRepository(session)

# 2. Зависимость для Менеджера (ждет Кладовщика)
def get_habit_service(repository: HabitRepository = Depends(get_habit_repository)) -> HabitService:
    return HabitService(repository)