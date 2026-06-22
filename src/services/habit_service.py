from src.database.repository import HabitRepository
from src.schemas import HabitCreate


class HabitService:
    def __init__(self, repository: HabitRepository):
        self.repository = repository
    async def create_habit(self, habit_data: HabitCreate):
        """бизнес логика"""
        return await self.repository.create(habit_data)
    async def get_habits(self):
        return await self.repository.get_all()