import uuid
from src.schemas import HabitCreate, HabitUpdate
from src.database.repository import HabitRepository
from src.exceptions import HabitAlreadyExistsError, HabitNotFoundError

class HabitService:
    def __init__(self, repository: HabitRepository):
        self.repository = repository

    async def create_habit(self, habit_data: HabitCreate):
        existing_habit = await self.repository.get_by_title(habit_data.title)
        if existing_habit:
            # Выбрасываем чистую ошибку бизнес-логики
            raise HabitAlreadyExistsError(f"Привычка '{habit_data.title}' уже существует.")

        return await self.repository.create(habit_data)

    async def get_all_habits(self, offset: int = 0, limit: int = 20):
        return await self.repository.get_all(offset=offset, limit=limit)

    async def update_habit(self, habit_id: uuid.UUID, update_data: HabitUpdate):
        habit = await self.repository.get_by_id(habit_id)
        if not habit:
            raise HabitNotFoundError("Привычка не найдена")

        if update_data.title and update_data.title != habit.title:
            existing = await self.repository.get_by_title(update_data.title)
            if existing:
                raise HabitAlreadyExistsError("Это название уже занято")

        update_dict = update_data.model_dump(exclude_unset=True)
        return await self.repository.update(habit, update_dict)

    async def delete_habit(self, habit_id: uuid.UUID):
        habit = await self.repository.get_by_id(habit_id)
        if not habit:
            raise HabitNotFoundError("Привычка не найдена")

        await self.repository.delete(habit)