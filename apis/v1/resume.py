from fastapi import APIRouter, status

from llm.chatModel import ChatModel
from manager.job import Job as JobManager
from respones.generic_response import GenericResponse
from manager.resume import Resume

resumeRouter = APIRouter(prefix="/resumes",tags=["简历相关"])

@resumeRouter.post("/", status_code=status.HTTP_201_CREATED,   responses={status.HTTP_201_CREATED: {"model": GenericResponse[str]},
                        status.HTTP_409_CONFLICT: {"model": GenericResponse}}, summary="申请岗位")
def apply_job(job_id:str):
    manager = JobManager()
    job_object=manager.get_job(job_id)
    chatModel = ChatModel(verbose=True)
    chatModel = ChatModel(verbose=True)
    model = chatModel.get()
    resume = Resume(model)
    resume_text = resume.read_resume()
    vectorstore = resume.get_vectorstore("yanzhiwei",resume_text)
    manager=JobManager()
    letter = resume.get_self_introduction(vectorstore, job_object)
    return GenericResponse[str](data=letter)