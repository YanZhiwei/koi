from dataclasses import dataclass

from models.boss import Boss
from models.job_summary import JobSummary


@dataclass(init=False)
class Job:
    id: str = ""
    summary: JobSummary = None
    boss: Boss = None
    detail: str = ""
    posted_date: str = ""

    def __init__(
        self,
        id: str = "",
        summary: JobSummary = None,
        boss: Boss = None,
        detail: str = "",
        posted_date: str = "",
    ):
        self.id = id
        self.summary = summary
        self.boss = boss
        self.detail = detail
        self.posted_date = posted_date
