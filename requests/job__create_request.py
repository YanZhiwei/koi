from typing import List

from pydantic import BaseModel, Field


class CreateJobRequest(BaseModel):
    id: str = Field(..., min_length=2,max_length=255)
    detail: str = Field(..., min_length=2)
    posted_date: str = Field(..., min_length=2,max_length=32)
    title: str =  Field(..., min_length=2,max_length=255)
    url: str = Field(..., min_length=2,max_length=255)
    company: str = Field(..., min_length=2)
    area: str =Field(..., min_length=2)
    tags: List[str] = None
    salary: str =Field(..., min_length=2,max_length=32)
    search_keywords: str =Field(..., min_length=2)
    boss_name: str = Field(..., min_length=2)
    boss_title: str = Field(..., min_length=2)
    boss_active_state: str = Field(..., min_length=2)
    
