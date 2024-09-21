from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from dtos.create_rpa_task_dto import CreateRpaTaskDto
from requests.create_rpa_task_request import CreateRpaTaskRequest

rpaRouter = APIRouter(tags=["RPA相关"])
from uuid import uuid4


@rpaRouter.post("/job/{id}", response_model=CreateRpaTaskDto, summary="创建rpa任务")
def get_job(request: CreateRpaTaskRequest = Body(...), db: Session = Depends(get_db)):
    guid = uuid4()
    return CreateRpaTaskDto(id=guid)
