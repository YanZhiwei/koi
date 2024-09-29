from exception.job import JobNotFountException
from schemas.job__create import CreateJobRequest
from models.job_boss import Job_Boss as DB_Job_Boss_Schema
from models.job import Job as DB_Job_Schema


class Job(object):
    
    def create_job(self,request: CreateJobRequest)->DB_Job_Schema:
        job = DB_Job_Schema()
        job.area = request.area
        job.company = request.company
        job.detail = request.detail
        job.id = request.id
        job.posted_date = request.posted_date
        job.salary = request.salary
        job.search_keywords = request.search_keywords
        job.tags = ",".join(request.tags)
        job.title = request.title
        job.url=request.url
        job.add()
        
        job_boss = DB_Job_Boss_Schema()
        job_boss.id=request.id
        job_boss.name=request.boss_name
        job_boss.title=request.boss_title
        job_boss.active_state=request.boss_active_state
        job_boss.add()
        return job
        
    def get_job(self,id: str)->DB_Job_Schema:
        job = DB_Job_Schema.get_by_id(id)
        if not job:
            raise JobNotFountException(message="job %s not found." % id)
        return job
            