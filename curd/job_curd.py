from sqlalchemy.orm import Session

from database.database import get_db
from models.job import Job
from schemas.job_schema import Job as JobSchema


async def create_job(job: Job, db: Session = next(get_db())) -> JobSchema:
    jobSchema = JobSchema()
    jobSchema.id = job.summary.id
    jobSchema.name = job.summary.name
    jobSchema.url = job.summary.url
    jobSchema.detail = job.detail
    jobSchema.area = job.summary.area
    jobSchema.posted_date = job.posted_date
    jobSchema.language = job.summary.language
    jobSchema.salary = job.summary.salary
    jobSchema.tags = ", ".join(job.summary.tags)
    jobSchema.company = job.summary.company
    jobSchema.language = job.summary.language
    db.add(jobSchema)
    db.commit()
    db.refresh(jobSchema)
    return jobSchema


async def get_job(id: str, db: Session = next(get_db())) -> JobSchema:
    return db.query(JobSchema).filter(JobSchema.id == id).first()


async def exists_job(id: str, db: Session = next(get_db())) -> bool:
    return db.query(JobSchema).filter(JobSchema.id == id).first() != None
