from enum import Enum

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from schemas.base_schema import Base


class TaskStatus(Enum):
    PENDING = 1
    RUNNING = 2
    SUCCESS = 3
    FAILED = 4


class RpaTask(Base):
    __tablename__ = "rpa_task"
    id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    action = Column(String(50), nullable=False)
    data: Mapped[str] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.PENDING)
    retry: Mapped[int] = mapped_column(default=0)
