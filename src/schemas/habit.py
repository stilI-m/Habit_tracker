import uuid
from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime

class HabitBase(BaseModel):
    # Добавили min_length=1
    title: str = Field(..., min_length=1, max_length=100, description="Название привычки")
    description: str | None = Field(default=None, description="Подробное описание")

    # Кастомный валидатор (Сработает ПЕРЕД тем, как Pydantic пропустит данные)
    @field_validator('title')
    @classmethod
    def title_must_not_be_blank(cls, v: str) -> str:
        stripped = v.strip() # Отрезаем пробелы по краям
        if not stripped:
            raise ValueError('Название не может быть пустым или состоять только из пробелов')
        return stripped # Возвращаем очищенную от лишних пробелов строку

class HabitCreate(HabitBase):
    pass

# НОВАЯ СХЕМА: Больше не наследуемся от HabitBase, Она полностью самостоятельна.
class HabitUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None)

    @field_validator('title')
    @classmethod
    def title_must_not_be_blank(cls, v: str | None) -> str | None:
        # Для обновления title может быть None (если его не хотят менять)
        if v is not None:
            stripped = v.strip()
            if not stripped:
                raise ValueError('Название не может быть пустым или состоять только из пробелов')
            return stripped
        return v

class HabitResponse(HabitBase):
    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PaginationParams(BaseModel):
    offset: int = Field(default=0, ge=0, description="Сколько записей пропустить")
    # Жестко ограничиваем: отдаем не больше 100 записей за раз
    limit: int = Field(default=20, ge=1, le=100, description="Сколько записей вернуть")