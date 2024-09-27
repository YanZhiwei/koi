
from sqlalchemy import Column, String

from schema.base_schema import ModelBase, ModelDB


class Job_Boss(ModelBase, ModelDB):
    __tablename__ = "job_boss"
    id=Column("id", String(64), primary_key=True, nullable=False, comment="id")
    name= Column("name", String(32),nullable=False, comment="面试官姓名")
    active_state=Column("active_state", String(32),nullable=True, comment="活跃状态")
    title=Column("title", String(32),nullable=True, comment="面试官职位")
