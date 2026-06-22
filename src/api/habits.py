from fastapi import APIRouter, Depends
from src.schemas import HabitCreate, HabitResponse
from src.services.habit_service import HabitService
from src.dependencies import get_habit_service

# Создаем роутер с префиксом
router = APIRouter(prefix="/habits", tags=["Habits"])

@router.post("/", response_model=HabitResponse, status_code=201)
async def create_habit(
    habit_data: HabitCreate, # FastAPI сам проверит JSON через Pydantic
    service: HabitService = Depends(get_habit_service) # Получаем готового Менеджера
    ):
    """Создать новую привычку"""
    return await service.create_habit(habit_data)

@router.get("/", response_model=list[HabitResponse])
async def get_habits(
    service: HabitService = Depends(get_habit_service)
):
    """Получить список всех привычек"""
    return await service.get_habits()