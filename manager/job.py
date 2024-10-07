from exception.job import JobNotFountException
from models.job import Job as DB_Job
from models.job_boss import Job_Boss as DB_Job_Boss
from models.job_chat import Job_Chat as DB_Job_Chat
from schemas.job__create import CreateJobRequest


class Job(object):
    
    def create_job(self,request: CreateJobRequest)->DB_Job:
        job = DB_Job()
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
        
        job_boss = DB_Job_Boss()
        job_boss.id=request.id
        job_boss.name=request.boss_name
        job_boss.title=request.boss_title
        job_boss.active_state=request.boss_active_state
        job_boss.add()
        return job
        
    def get_job(self,id: str)->DB_Job:
        job = DB_Job.get_by_id(id)
        if not job:
            raise JobNotFountException(message="job %s not found." % id)
        return job
    
    def get_unchat_jobs(self,resume_id:str)->list[DB_Job]:
        chat_jobs = DB_Job_Chat.get_by_conditions(resume_id=resume_id)
        jobs=DB_Job.get_all()
        chat_job_ids=[chat_job.job_id for chat_job in chat_jobs]
        return [job for job in jobs if job.id not in chat_job_ids]
        