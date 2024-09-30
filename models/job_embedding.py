from sqlalchemy import Column, String

from models.model_base import ModelBase, ModelDB


class Job_Embedding(ModelBase, ModelDB):
    __tablename__ = "job_embedding"
    id=Column("id", String(64), primary_key=True, nullable=False, comment="id")
    model_name=Column("model_name", String(32),nullable=False, comment="模型名称")