

from automations.zhipin import Zhipin
from database.database import engine
from models.job_summary import JobSummary
from schemas.base_schema import Base
from schemas.job_boss_schema import Job_Boss
from schemas.job_schema import Job


async def main():
    zhipin = Zhipin("北京")
    await zhipin.search("python")
    job_summary = JobSummary()
    job_summary.area = "北京"
    job_summary.url = (
        "https://www.zhipin.com/job_detail/ece6ae88a5de57611XZy2dW-EVJZ.html"
    )
    await zhipin.get_job(job_summary)


if __name__ == "__main__":
    Base.metadata.create_all(engine, tables=[Job.__table__, Job_Boss.__table__])
    # asyncio.get_event_loop().run_until_complete(main())
