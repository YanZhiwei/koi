from fastapi import APIRouter, status

from manager.job import Job as JobManager
from requests.job__create_request import CreateJobRequest
from respones.generic_response import GenericResponse
from respones.job import JobDetail
from schema.job_schema import Job

jobRouter = APIRouter(prefix="/jobs",tags=["岗位相关"])


@jobRouter.get("/{id}", response_model=GenericResponse[JobDetail], summary="根据id获取job详情")
def get_job(id: str):
    manager = JobManager()
    job=manager.get_job(id)
    return GenericResponse[JobDetail](data=job)


@jobRouter.post("/", status_code=status.HTTP_201_CREATED,   responses={status.HTTP_201_CREATED: {"model": GenericResponse[JobDetail]},
                        status.HTTP_409_CONFLICT: {"model": GenericResponse}}, summary="创建job")
def create_job(request: CreateJobRequest):
    manager = JobManager()
    job=manager.create_job(request)
    return GenericResponse[JobDetail](data=job)
