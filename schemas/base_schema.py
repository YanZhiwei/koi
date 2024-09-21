from sqlalchemy import TIMESTAMP, Column, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __abstract__ = True
    create_at = Column(
        TIMESTAMP(timezone=True), default=func.now(tz="Asia/Shanghai"), nullable=False
    )
    update_dt = Column(
        TIMESTAMP(timezone=True),
        default=func.now(tz="Asia/Shanghai"),
        onupdate=func.now(tz="Asia/Shanghai"),
        nullable=False,
    )
