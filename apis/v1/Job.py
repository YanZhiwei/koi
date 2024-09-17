
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from curd import job_curd
from database.database import get_db
from dtos.job_dto import JobDto

jobRouter = APIRouter(tags=["岗位相关"])


@jobRouter.get("/job/{id}", response_model=JobDto, summary="根据id获取job详情")
async def get_job(id: str, db: Session = Depends(get_db)):
    job_schema = await job_curd.get_job(id, db)
    if job_schema is None:
        raise HTTPException(status_code=404, detail="Job not found")
    job_dto = JobDto(
        id=job_schema.id,
        name=job_schema.name,
        url=job_schema.url,
        salary=job_schema.salary,
        posted_date=job_schema.posted_date,
        area=job_schema.area,
        tags=job_schema.tags,
        detail=job_schema.detail,
        company=job_schema.company,
        language=job_schema.language,
    )

    return job_dto
