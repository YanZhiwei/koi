import asyncio

from automations.zhipin import Zhipin
from models.job_summary import JobSummary


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
    asyncio.get_event_loop().run_until_complete(main())
