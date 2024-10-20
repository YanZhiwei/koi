import asyncio
import json
import random
import threading
import time

import schedule
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from apis.v1.job import jobRouter
from apis.v1.resume import resumeRouter
from conf.config import log_configs
from database.database import engine
from llm.chatModel import ChatModel
from manager.job import Job as JobManager
from manager.job_chat import Job_Chat as Job_ChatManager
from manager.resume import Resume
from models.job import Job
from models.job_boss import Job_Boss
from models.job_chat import Job_Chat
from models.model_base import ModelBase
from schemas.job_chat_create import CreateJobChatRequest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(jobRouter)
app.include_router(resumeRouter)

@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to my Page"}

def job():
    try:
        print("Executing scheduled job...")
        chat_manager=Job_ChatManager()
        job_manager=JobManager()
        chatModel = ChatModel(verbose=True)
        model = chatModel.get()
        resume = Resume(model)
        resume_text = resume.read_resume()
        vectorstore = resume.get_vectorstore("yanzhiwei",resume_text)
        unchat_jobs=job_manager.get_unchat_jobs()
        for job in unchat_jobs:
            id=f'{job.id}_yanzhiwei'
            if chat_manager.exist_job_chat(job.id)==False:
                job = job_manager.get_job(job.id)
                letter = resume.get_self_introduction(vectorstore, job)
                chat_manager.create_job_chat(
                    request=CreateJobChatRequest(
                        job_id=job.id,
                        llm_model=json.dumps( model.model_config,ensure_ascii=False),
                        id=id,
                        resume_name="yanzhiwei",
                        self_introduce=letter,
                    )
                )
            logger.info(f"{job.title} chat created")
    except Exception as e:
        print(e)
    
    
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)  #

schedule.every().day.at("07:00").do(job)

async def async_job():
    try:
        print("Executing scheduled job...")
        chat_manager=Job_ChatManager()
        job_manager=JobManager()
        chatModel = ChatModel(verbose=True)
        model = chatModel.get()
        resume = Resume(model,"2024-言志伟-研发简历.pdf")
        vectorstore = resume.get_vectorstore()
        unchat_jobs=job_manager.get_unchat_jobs(resume.key)
        for job in unchat_jobs:
            try:
                id=f'{resume.key}_{job.id}'
                if chat_manager.exist_job_chat(job.id)==False:
                    job = job_manager.get_job(job.id)
                    letter = resume.get_self_introduction(vectorstore, job)
                    chat_manager.create_job_chat(
                        request=CreateJobChatRequest(
                            job_id=job.id,
                            llm_model=model.model,
                            id=id,
                            resume_id=resume.key,
                            resume_name=resume.resume_pdf,
                            self_introduce=letter,
                        )
                    )
                    logger.info(f"{job.title} chat created")
                    random_sleep_time = random.randint(5, 20)
                    await asyncio.sleep(random_sleep_time)
                else:
                    logger.info(f"{job.title} chat already exists")
            except Exception as e:
                logger.error(f"{job.title} chat failed,detail: {e}")
    except Exception as ee:
        logger.error(f"Executing scheduled job chat failed,detail: {ee}")
def schedule_async_job():
    asyncio.create_task(async_job())
    
if __name__ == "__main__":
    
    logger.configure(**log_configs)
    ModelBase.metadata.create_all(
        engine, tables=[Job.__table__, Job_Boss.__table__,Job_Chat.__table__]
    )
    logger.info("Database created")
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True  
    scheduler_thread.start()
    asyncio.run(async_job())
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
