import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from apis.v1.job import jobRouter
from conf.config import log_configs
from database.database import engine
from models.model_base import ModelBase
from models.job_boss import Job_Boss
from models.job import Job

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


if __name__ == "__main__":
    logger.configure(**log_configs)
    ModelBase.metadata.create_all(
        engine, tables=[Job.__table__, Job_Boss.__table__]
    )
    logger.info("Database created")
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
