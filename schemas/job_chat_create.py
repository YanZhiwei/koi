from typing import List

from pydantic import BaseModel, Field


class CreateJobChatRequest(BaseModel):
    id:str= Field(..., min_length=2)
    job_id: str = Field(..., min_length=2)
    resume_id: str = Field(..., min_length=2)
    resume_name: str = Field(..., min_length=2)
    llm_model: str = Field(..., min_length=2)
    self_introduce: str = Field(..., min_length=2)
