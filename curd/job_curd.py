from sqlalchemy.orm import Session

from database.database import get_db
from models.job import Job
from schemas.job_boss_schema import Job_Boss as Job_Boss_Schema
from schemas.job_schema import Job as JobSchema


def create_job(job: Job, db: Session = next(get_db())) -> JobSchema:
    # db.begin()
    try:
        jobSchema: JobSchema = JobSchema()
        jobSchema.id = job.summary["id"]
        jobSchema.name = job.summary["name"]
        jobSchema.url = job.summary["url"]
        jobSchema.detail = job.detail
        jobSchema.area = job.summary["area"]
        jobSchema.posted_date = job.posted_date
        jobSchema.language = job.summary["language"]
        jobSchema.salary = job.summary["salary"]
        jobSchema.tags = ", ".join(job.summary["tags"])
        jobSchema.company = job.summary["company"]
        jobSchema.language = job.summary["language"]
        job_Boss_Schema = Job_Boss_Schema()
        job_Boss_Schema.id = job.summary["id"]
        job_Boss_Schema.name = job.boss["name"]
        job_Boss_Schema.title = job.boss["title"]
        job_Boss_Schema.active_state = job.boss["active_state"]
        db.add(jobSchema)
        db.add(job_Boss_Schema)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return jobSchema


def get_job(id: str, db: Session = next(get_db())) -> JobSchema:
    return db.query(JobSchema).filter(JobSchema.id == id).first()


def exists_job(id: str, db: Session = next(get_db())) -> bool:
    return db.query(JobSchema).filter(JobSchema.id == id).first() != None
