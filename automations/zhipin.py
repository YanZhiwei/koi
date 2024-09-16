from typing import List

from playwright.async_api import async_playwright

from chrome import get_chrome_path_windows
from models.job import Job
from models.job_summary import JobSummary


class Zhipin(object):

    def __init__(
        self,
        city: str,
    ):
        self.url = "https://www.zhipin.com/"
        self.city = city
        self.browser = None

    def __del__(self):
        self.browser.close()

    async def __instance_browser(self):
        chrome_path = get_chrome_path_windows()
        if chrome_path is None:
            raise Exception("chrome path not found")
        p = await async_playwright().start()
        self.browser = await p.chromium.launch(
            executable_path=chrome_path,
            headless=False,
            args=["--disable-infobars"],
            ignore_default_args=["--enable-automation"],
        )

    async def search(self, keyword: str) -> List[JobSummary]:
        jobSummarys: List[JobSummary] = []
        if not self.browser:
            await self.__instance_browser()
        page = await self.browser.new_page()
        await page.goto(
            "https://www.zhipin.com/shanghai/?seoRefer=index",
            wait_until="domcontentloaded",
        )
        await page.type('[name="query"]', keyword)
        await page.click(".btn-search")
        await page.wait_for_selector(".job-list-box")
        job_result = await page.locator(".job-list-box > li").all()
        for job in job_result:
            job_name = await job.locator(".job-name").inner_text()
            job_area = await job.locator(".job-area").inner_text()
            job_link = await job.locator(".job-card-left").get_attribute("href")
            company_name = await job.locator(".company-name").inner_text()
            info_desc = await job.locator(".info-desc").inner_text()
            tag_list = await job.locator(".tag-list > li").all()
            tags = []
            for tag in tag_list:
                tag_text = await tag.inner_text()
                tags.append(tag_text)
            job_summary = JobSummary()
            job_summary.name = job_name
            job_summary.area = job_area
            job_summary.link = f"https://www.zhipin.com{job_link}"
            job_summary.company = company_name
            job_summary.tags = tags
            job_summary.description = info_desc
            jobSummarys.append(job_summary)
        return jobSummarys

    async def get_job(self, job_summary: JobSummary) -> Job:
        job: Job = None
        if not self.browser:
            await self.__instance_browser()
        page = await self.browser.new_page()
        await page.goto(
            job_summary.url,
            wait_until="domcontentloaded",
        )
        await page.wait_for_selector(".job-detail")
        job_summary = await page.locator(".job-detail").inner_html()
        posted_date = await page.locator(".gray").inner_text()
        job.detail = job_summary
        job.posted_date = posted_date
        return job
