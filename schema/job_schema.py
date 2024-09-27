
from sqlalchemy import Column, String, Text

from schema.base_schema import ModelBase, ModelDB


class Job(ModelBase, ModelDB):
    __tablename__ = "job"

    id=Column("id", String(64), primary_key=True, nullable=False, comment="id")
    title= Column("title", String(255),nullable=False, comment="岗位名称")
    url=Column("url", String(255),nullable=False, comment="岗位链接")
    company=Column("company", String(255),nullable=False, comment="公司名称")
    area=Column("area", String(255),nullable=False, comment="所在地区")
    salary= Column("salary", String(32),nullable=False, comment="薪资")
    tags= Column("tags", String(64),nullable=True, comment="标签")
    search_keywords=Column("search_keywords", String(255),nullable=True, comment="搜索关键词")
    detail= Column("detail",Text,nullable=True, comment="岗位详情")
    posted_date= Column("posted_date", String(32),nullable=True, comment="发布日期")
    
