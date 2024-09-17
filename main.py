import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apis.v1.Job import jobRouter
from automations.zhipin import Zhipin
from curd.job_curd import create_job
from database.database import engine, get_db
from models.job_summary import JobSummary
from schemas.base_schema import Base
from schemas.job_boss_schema import Job_Boss
from schemas.job_schema import Job

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(jobRouter)


@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to my Page"}


async def main():
    zhipin = Zhipin("北京")
    result = await zhipin.search("python")
    for job_summary in result:
        # job_summary = JobSummary()
        # job_summary.area = "北京"
        # job_summary.url = (
        #     "https://www.zhipin.com/job_detail/ece6ae88a5de57611XZy2dW-EVJZ.html"
        # )
        # job_summary.name = "Python编程老师"
        # job_summary.tags = ["python"]
        # job_summary.salary = "6k-8k"
        # job_summary.company = "百度"
        # job_summary.id = "ece6ae88a5de57611XZy2dW-EVJZ"
        # job_summary = job_summary
        job = await zhipin.get_job(job_summary)
        await create_job(job)


if __name__ == "__main__":
    Base.metadata.create_all(engine, tables=[Job.__table__, Job_Boss.__table__])
    # asyncio.get_event_loop().run_until_complete(main())
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
