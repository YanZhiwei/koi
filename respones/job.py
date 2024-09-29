from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from base.schemaMetaclass import SchemaMetaclass
from models.job import Job as DB_Job_Schema


class JobDetail(BaseModel):
    id:str = Field()
    title: str=Field()
    url: str=Field()
    company: str=Field()
    area: str=Field()
    salary:  str=Field()
    tags:  str=Field()
    search_keywords: str=Field()
    detail:  str=Field()
    posted_date: str=Field(max_length=32)
    # created_at: Optional[datetime] = Field()
    # updated_at: Optional[datetime] = Field()

        
    model_config = {
        
        "from_attributes": True  # 允许从非字典对象读取属性
    }