from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, delete, func, select, update
from sqlalchemy.orm import DeclarativeBase

from database.database import Session


class ModelBase(DeclarativeBase):
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

class ModelIterator(object):

    def __init__(self, model, columns):
        self.model = model
        self.i = columns

    def __iter__(self):
        return self

    def __next__(self):
        n = next(self.i)
        return n, getattr(self.model, n)

class ModelDB(object):
    def add(self):
        with Session(expire_on_commit=False) as session:  # expire_on_commit=False可以让self model对象属性依然可以访问
            with session.begin():
                session.add(self)
                return self

    @classmethod
    def delete(cls, **kwargs):
        filters = []
        for key, val in kwargs.items():
            if getattr(cls, key, None):
                filters.append(getattr(cls, key) == val)

        with Session() as session:
            query = delete(cls).where(*filters)
            rv = session.execute(query)
            session.commit()
        return rv.rowcount

    @classmethod
    def get_by_id(cls, uuid):
        with Session() as session:
            query = select(cls).where(getattr(cls, "id") == uuid)
            return session.execute(query).scalars().one_or_none()

    @classmethod
    def get_by_conditions(cls, **conditions):
        filters = []
        for key, val in conditions.items():
            if getattr(cls, key, None):
                filters.append(getattr(cls, key) == val)

        with Session() as session:
            query = select(cls).where(*filters)
            return session.execute(query).scalars().fetchall()

    @classmethod
    def get_all(cls):
        with Session() as session:
            query = select(cls)
            return session.execute(query).scalars().fetchall()

    @classmethod
    def get_by_page(cls, skip: int, limit: int):
        with Session() as session:
            query = select(cls).offset(skip).limit(limit)
            return session.execute(query).scalars().fetchall()

    @classmethod
    def update(cls, **kwargs):
        uuid = kwargs.pop("uuid")
        with Session(expire_on_commit=False) as session:
            query = update(cls).where(cls.uuid == uuid).values(**kwargs)
            rv = session.execute(query)
            session.commit()
            return rv.rowcount

    def as_dict(self, except_keys=()):
        """
        :param except_keys: 不期望返回的字段
        """
        local = {}
        for key, value in self:  # 需要实现__iter__
            if key in except_keys:
                continue
            elif isinstance(value, datetime):
                value = int(value.timestamp())  # 转为时间戳
            local[key] = value

        return local

    def iteritems(self):
        """Make the model object behave like a dict."""
        return self.as_dict().items()

    def items(self):
        """Make the model object behave like a dict."""
        return self.as_dict().items()

    def keys(self):
        """Make the model object behave like a dict."""
        return [key for key, value in self.iteritems()]

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __contains__(self, key):
        # Don't use hasattr() because hasattr() catches any exception, not only
        # AttributeError. We want to passthrough SQLAlchemy exceptions
        # (ex: sqlalchemy.orm.exc.DetachedInstanceError).
        try:
            getattr(self, key)
        except AttributeError:
            return False
        else:
            return True

    def __iter__(self):
        columns = [prop.key for prop in self.__mapper__.iterate_properties]
        return ModelIterator(self, iter(columns))