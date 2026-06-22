import uuid
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class HabitBase(BaseModel):
    title: str = Field(..., max_length=100, description="Название привычки")
    description: str | None = Field(default=None, description="Подробное описание")
class HabitCreate(HabitBase):
    pass
class HabitUpdate(HabitBase):
    title: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None)
class HabitResponse(HabitBase):
    id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)