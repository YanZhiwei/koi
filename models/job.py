from dataclasses import dataclass
from datetime import datetime

from models.boss import Boss
from models.job_summary import JobSummary


@dataclass(init=False)
class Job:
    id: str = ""
    summary: JobSummary = None
    boss: Boss = None
    detail: str = ""
    posted_date: str = ""
    boss: Boss = None
