import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Habit
from src.schemas import HabitCreate, HabitUpdate


class HabitRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def create(self, habit_data: HabitCreate) -> Habit:
        """Создает привычку"""
        new_habit = Habit(title = habit_data.title, description = habit_data.description)
        self.session.add(new_habit)
        await self.session.commit()
        await self.session.refresh(new_habit)
        return new_habit
    async def get_all(self) -> list[Habit]:
        """Возвращает все привычки"""
        query = select(Habit)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    async def update(self, habit: Habit, update_data: dict) -> Habit:
        """Принимает готовый объект базы и словарь с новыми данными."""
        for key, value in update_data.items():
            setattr(habit, key, value)
        await self.session.commit()
        await self.session.refresh(habit)
        return habit
    async def delete(self, habit: Habit) -> None:
        """Удаляет объект из базы."""
        await self.session.delete(habit)
        await self.session.commit()
    async def get_by_id(self, habit_id: uuid.UUID) -> Habit | None:
        """Ищет привычку по ID. Возвращает None, если не нашел."""
        query = select(Habit).where(Habit.id == habit_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    async def get_by_title(self, title: str) -> Habit | None:
        """Ищет привычку по точному совпадению названия."""
        query = select(Habit).where(Habit.title == title)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

