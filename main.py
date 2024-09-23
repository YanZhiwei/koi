import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apis.v1.job import jobRouter
from apis.v1.rpa import rpaRouter
from database.database import engine
from schemas.base_schema import Base
from schemas.job_boss_schema import Job_Boss
from schemas.job_schema import Job
from schemas.rpa_task_schema import RpaTask

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(jobRouter)
app.include_router(rpaRouter)


@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to my Page"}


if __name__ == "__main__":
    Base.metadata.create_all(
        engine, tables=[Job.__table__, Job_Boss.__table__, RpaTask.__table__]
    )
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
