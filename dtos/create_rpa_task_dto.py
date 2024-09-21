from uuid import UUID

from pydantic import BaseModel, Field


class CreateRpaTaskDto(BaseModel):
    id: UUID = Field(..., description="The unique identifier for the RPA task")
