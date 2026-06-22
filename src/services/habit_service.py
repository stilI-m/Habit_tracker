import uuid

from fastapi import HTTPException, status
from src.database.repository import HabitRepository
from src.schemas import HabitCreate, HabitUpdate


class HabitService:
    def __init__(self, repository: HabitRepository):
        self.repository = repository
    async def create_habit(self, habit_data: HabitCreate):
        # 1. Проверяем, есть ли уже такая привычка
        existing_habit = await self.repository.get_by_title(habit_data.title)
        if existing_habit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Привычка с таким названием уже существует."
            )

        return await self.repository.create(habit_data)
    async def get_habits(self):
        return await self.repository.get_all()
    async def update_habit(self, habit_id: uuid.UUID, update_data: HabitUpdate):
        # 1. Ищем привычку. Если нет — отдаем 404
        habit = await self.repository.get_by_id(habit_id)
        if not habit:
            raise HTTPException(status_code=404, detail="Привычка не найдена")

        # 2. Если пользователь хочет изменить название, проверяем, не занято ли оно
        if update_data.title and update_data.title != habit.title:
            existing = await self.repository.get_by_title(update_data.title)
            if existing:
                raise HTTPException(status_code=400, detail="Это название уже занято")

        # 3. Убираем поля со значением None (чтобы не перезаписать данные пустотой)
        update_dict = update_data.model_dump(exclude_unset=True)

        return await self.repository.update(habit, update_dict)
    async def delete_habit(self, habit_id: uuid.UUID):
        # Проверяем существование перед удалением
        habit = await self.repository.get_by_id(habit_id)
        if not habit:
            raise HTTPException(status_code=404, detail="Привычка не найдена")

        await self.repository.delete(habit)