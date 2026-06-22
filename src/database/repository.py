
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Habit
from src.schemas import HabitCreate


class HabitRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def create(self, habit_data: HabitCreate) -> Habit:
        new_habit = Habit(title = habit_data.title, description = habit_data.description)
        self.session.add(new_habit)
        await self.session.commit()
        await self.session.refresh(new_habit)
        return new_habit
    async def get_all(self) -> list[Habit]:
        query = select(Habit)
        result = await self.session.execute(query)
        return list(result.scalars().all())