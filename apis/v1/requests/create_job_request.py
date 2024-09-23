from pydantic import BaseModel, Field

from models.boss import Boss
from models.job_summary import JobSummary


class CreateJobRequest(BaseModel):
    id: str = Field(..., min_length=2, description="岗位id")
    summary: JobSummary = None
    boss: Boss = None
    detail: str = Field(..., min_length=2, description="岗位详情")
    posted_date: str = Field(..., min_length=2, description="岗位更新时间")
