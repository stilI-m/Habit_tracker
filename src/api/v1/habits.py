import uuid
from fastapi import APIRouter, Depends, status, Response, HTTPException
from src.schemas.habit import HabitCreate, HabitResponse, HabitUpdate, PaginationParams
from src.services.habit_service import HabitService
from src.core.dependencies import get_habit_service
from src.exceptions import HabitAlreadyExistsError, HabitNotFoundError

router = APIRouter(prefix="/habits", tags=["Habits"])

@router.post("/", response_model=HabitResponse, status_code=201)
async def create_habit(
    habit_data: HabitCreate,
    service: HabitService = Depends(get_habit_service)
):
    try:
        return await service.create_habit(habit_data)
    except HabitAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=list[HabitResponse])
async def get_habits(
    pagination: PaginationParams = Depends(), # Получаем параметры от пользователя
    service: HabitService = Depends(get_habit_service)
):
    """Получить список привычек (с пагинацией)"""
    return await service.get_all_habits(
        offset=pagination.offset,
        limit=pagination.limit
    )

@router.patch("/{habit_id}", response_model=HabitResponse)
async def update_habit(
    habit_id: uuid.UUID,
    update_data: HabitUpdate,
    service: HabitService = Depends(get_habit_service)
):
    try:
        return await service.update_habit(habit_id, update_data)
    except HabitNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except HabitAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_habit(
    habit_id: uuid.UUID,
    service: HabitService = Depends(get_habit_service)
):
    try:
        await service.delete_habit(habit_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HabitNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))