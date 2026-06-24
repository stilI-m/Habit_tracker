from datetime import datetime
import uuid
from sqlalchemy import String, DateTime, Text, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class Habit(Base):
    __tablename__ = 'habits'
    __table_args__ = (
        UniqueConstraint('title', name='uq_habit_title'),
    )
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
