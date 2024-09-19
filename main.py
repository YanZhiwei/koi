import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apis.v1.job import jobRouter
from automations.zhipin import Zhipin
from curd.job_boss_curd import create_job_boss
from curd.job_curd import create_job, exists_job
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
    count: int = len(result)
    print(f"Found {count} jobs")
    add_jobs_count: int = 0
    exists_job_count: int = 0
    for job_summary in result:
        exist = exists_job(job_summary.id)
        if exist == False:
            job = await zhipin.get_job(job_summary)
            create_job(job)
            create_job_boss(job)
            add_jobs_count += 1
            print(f"Job:{job_summary.id} added")
        else:
            print(f"Job:{job_summary.id} already exists")
            exists_job_count += 1
    print(f"Added {add_jobs_count} jobs,exist:{exists_job_count} jobs")


if __name__ == "__main__":
    Base.metadata.create_all(engine, tables=[Job.__table__, Job_Boss.__table__])
    asyncio.get_event_loop().run_until_complete(main())
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
