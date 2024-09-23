from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from apis.v1.requests.create_rpa_task_request import CreateRpaTaskRequest
from curd import rpa_task_curd
from database.database import get_db
from dtos.create_rpa_task_dto import CreateRpaTaskDto
from models.rpa_task import RpaTask

rpaRouter = APIRouter(tags=["RPA相关"])
import uuid
from uuid import uuid4


@rpaRouter.post("/search/job", response_model=CreateRpaTaskDto, summary="创建rpa任务")
def search_job(
    request: CreateRpaTaskRequest = Body(...), db: Session = Depends(get_db)
):
    data = request.model_dump_json(indent=1).upper()
    action = "search_job"
    exist_task = rpa_task_curd.get_rpa_task(action=action, data=data, db=db)
    id = uuid4()
    if exist_task is None:
        rpa_task: RpaTask = RpaTask()
        rpa_task.action = action
        rpa_task.data = data
        rpa_task.id = str(id)
        rpa_task_curd.create_rpa_task(rpa_task, db)
    else:
        id = uuid.UUID(exist_task.id)
    return CreateRpaTaskDto(id=id)
