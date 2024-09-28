from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from base.schemaMetaclass import SchemaMetaclass
from schema.job_schema import Job as DB_Job_Schema


class JobDetail(BaseModel, metaclass=SchemaMetaclass):
    id:str = Field(max_length=64)
    title: str=Field(max_length=255)
    url: str=Field(max_length=255)
    company: str=Field(max_length=255)
    area: str=Field(max_length=255)
    salary:  str=Field(max_length=32)
    tags:  str=Field(max_length=255)
    search_keywords: str=Field(max_length=255)
    detail:  str=Field()
    posted_date: str=Field(max_length=32)
    created_at: Optional[datetime] = Field()
    updated_at: Optional[datetime] = Field()
    class Config:
        orm_mode = True
        orm_model = DB_Job_Schema