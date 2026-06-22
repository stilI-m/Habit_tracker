import uuid

from fastapi import APIRouter, Depends, Response, status


from src.schemas import HabitCreate, HabitResponse, HabitUpdate
from src.services.habit_service import HabitService
from src.dependencies import get_habit_service

# Создаем роутер с префиксом
router = APIRouter(prefix="/habits", tags=["Habits"])

@router.get("/", response_model=list[HabitResponse])
async def get_habits(
    service: HabitService = Depends(get_habit_service)
):
    """Получить список всех привычек"""
    return await service.get_habits()

@router.post("/", response_model=HabitResponse, status_code=201)
async def create_habit(
    habit_data: HabitCreate, # FastAPI сам проверит JSON через Pydantic
    service: HabitService = Depends(get_habit_service) # Получаем готового Менеджера
    ):
    """Создать новую привычку"""
    return await service.create_habit(habit_data)

@router.patch("/{habit_id}", response_model=HabitResponse)
async def update_habit(
    habit_id: uuid.UUID,
    update_data: HabitUpdate,
    service: HabitService = Depends(get_habit_service)
):
    """Частично обновить привычку"""
    return await service.update_habit(habit_id, update_data)

@router.delete("/{habit_id}", response_model=HabitResponse)
async def delete_habit(
    habit_id: uuid.UUID,
    service: HabitService = Depends(get_habit_service)
):
    """Удалить привычку"""
    await service.delete_habit(habit_id)
    # Метод DELETE по стандарту REST возвращает пустой ответ с кодом 204
    return Response(status_code=status.HTTP_204_NO_CONTENT)




