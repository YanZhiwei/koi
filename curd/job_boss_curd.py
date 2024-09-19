from sqlalchemy.orm import Session

from database.database import get_db
from models.job import Job
from schemas.job_boss_schema import Job_Boss as Job_Boss_Schema


def create_job_boss(job: Job, db: Session = next(get_db())) -> Job_Boss_Schema:
    job_Boss_Schema = Job_Boss_Schema()
    job_Boss_Schema.id = job.summary.id
    job_Boss_Schema.name = job.boss.name
    job_Boss_Schema.title = job.boss.title
    job_Boss_Schema.active_state = job.boss.active_state
    db.add(job_Boss_Schema)
    db.commit()
    db.refresh(job_Boss_Schema)
    return job_Boss_Schema
