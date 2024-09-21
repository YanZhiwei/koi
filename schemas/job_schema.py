from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from schemas.base_schema import Base


class Job(Base):
    __tablename__ = "job"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    url: Mapped[str] = mapped_column(String(256))
    company: Mapped[str] = mapped_column(String(100))
    area: Mapped[str] = mapped_column(String(100))
    salary: Mapped[str] = mapped_column(String(25))
    tags: Mapped[str] = mapped_column(String(100))
    language: Mapped[str] = mapped_column(String(25))
    detail: Mapped[str] = Column(Text)
    posted_date: Mapped[str] = mapped_column(String(25))
