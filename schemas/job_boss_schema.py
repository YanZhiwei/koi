from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from schemas.base_schema import Base


class Job_Boss(Base):
    __tablename__ = "job_boss"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    create_at: Mapped[DateTime] = mapped_column(
        DateTime(), default=datetime.now(timezone.utc)
    )
    active_state: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(100), index=True)
