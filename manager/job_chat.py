from models.job_chat import Job_Chat as DB_Job_Chat
from schemas.job_chat_create import CreateJobChatRequest


class Job_Chat(object):
    
    def create_job_chat(self,request: CreateJobChatRequest)->DB_Job_Chat:
        job_chat = DB_Job_Chat()
        job_chat.id=request.id
        job_chat.job_id=request.job_id
        job_chat.model_name=request.model_name
        job_chat.resume_name=request.resume_name
        job_chat.self_introduce=request.self_introduce
        job_chat.add()
        return 
    
    def exist_job_chat(self,id: str)->bool:
        job_chat = DB_Job_Chat.get_by_id(id)
        if job_chat:
            return True
        return False