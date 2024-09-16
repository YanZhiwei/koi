import asyncio

from automations.zhipin import Zhipin
from models.job_summary import JobSummary


async def main():
    zhipin = Zhipin("北京")
    await zhipin.search("python")
    # job_summary = JobSummary()
    # job_summary.area = "北京"
    # job_summary.url = "https://www.zhipin.com/job_detail/3e18a20d09bbf2eb1HZ73tS-F1BS.html?lid=6MCzp086K5Q.search.1&securityId=G8sWJQTyzxDnE-21O_5Oo_R3UAU8Kf5bYWPhyc_BOkDP6q17cZzZx_P-1qV_XNo7-Qo_Drjl2sJht5V5q6M7s8-oVmd2TCTP5lGoko0CW7brzj5b2ks~&sessionId="
    # # await zhipin.get_job(job_summary)
    # await zhipin.search("python")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    
