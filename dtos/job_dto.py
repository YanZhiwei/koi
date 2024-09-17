from pydantic import BaseModel


class JobDto(BaseModel):
    id: str
    name: str
    url: str
    salary: str
    posted_date: str
    area: str
    tags: str
    detail: str
    company: str
    language: str
