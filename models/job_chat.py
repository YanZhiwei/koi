from sqlalchemy import Column, String

from models.model_base import ModelBase, ModelDB


class Job_Chat(ModelBase, ModelDB):
    __tablename__ = "job_chat"
    id=Column("id", String(64), primary_key=True, nullable=False, comment="id")
    model_name=Column("model_name", String(32),nullable=False, comment="模型名称")
    resume_name=Column("resume_name", String(64),nullable=False, comment="简历名称")
    resume_id=Column("resume_id", String(32),nullable=False, comment="简历id")
    job_id=Column("job_id", String(64),nullable=False, comment="岗位id")
    self_introduce=Column("self_introduce", String(1024),nullable=False, comment="自我介绍")
    