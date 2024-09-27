from fastapi import APIRouter, status

from manager.job import Job as JobManager
from requests.job__create_request import CreateJobRequest
from respones.generic_response import GenericResponse
from schema.job_schema import Job

jobRouter = APIRouter(prefix="/jobs",tags=["岗位相关"])


@jobRouter.get("/{id}", response_model=GenericResponse[Job], summary="根据id获取job详情")
def get_job(id: str):
    manager = JobManager()
    job=manager.get_job(id)
    return GenericResponse[Job](data=job)


@jobRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=GenericResponse[Job], summary="创建job")
def create_job(request: CreateJobRequest):
    manager = JobManager()
    job=manager.create_job(request)
    return GenericResponse[Job](data=job)
