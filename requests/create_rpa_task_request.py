from pydantic import BaseModel, Field


class CreateRpaTaskRequest(BaseModel):
    title: str = Field(..., min_length=2, description="岗位名词")
    area: str
