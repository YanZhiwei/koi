from pydantic import BaseModel


class CreateRpaTaskRequest(BaseModel):
    title: str
    area: str
