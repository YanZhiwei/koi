import asyncio
import random
from typing import List
from urllib.parse import urlparse

from playwright.async_api import Page, async_playwright
from playwright.sync_api import BrowserContext

from chrome import get_chrome_path_windows
from models.boss import Boss
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
        self.context: BrowserContext = None

    async def __del__(self):
        await self.browser.close()

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
        self.context = await self.browser.new_context()

    async def close_login_dialog_if_exists(self, page: Page):
        try:
            if await page.locator(".boss-login-dialog").is_visible():
                await page.locator(".boss-login-close").click()
        except Exception as e:
            print(e)

    async def search(self, keyword: str) -> List[JobSummary]:
        jobSummarys: List[JobSummary] = []
        if not self.browser:
            await self.__instance_browser()
        page = await self.context.new_page()
        await page.goto(
            "https://www.zhipin.com/shanghai/?seoRefer=index",
            wait_until="domcontentloaded",
        )
        await page.type('[name="query"]', keyword)
        await page.click(".btn-search")
        await page.wait_for_selector(".job-list-box")
        search_url = page.url
        for i in range(1, 11):
            search_page_url = search_url + f"&page={i}"
            await page.goto(search_page_url, wait_until="domcontentloaded")
            await page.wait_for_selector(".job-list-box")
            await page.wait_for_selector(".job-list-box > li")
            await self.close_login_dialog_if_exists(page)
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
                job_summary.language = keyword
                job_summary.area = job_area
                job_summary.url = f"https://www.zhipin.com{job_link}"
                job_summary.company = company_name
                job_summary.salary = await job.locator(".salary").inner_text()
                job_summary.tags = tags
                job_summary.description = info_desc
                job_summary.id = self.__get__job_id(job_summary.url)
                jobSummarys.append(job_summary)
        return jobSummarys

    async def get_job(self, job_summary: JobSummary) -> Job:
        job: Job = Job()
        job.summary = job_summary
        job.id = job_summary.id
        if not self.browser:
            await self.__instance_browser()
        page = await self.context.new_page()

        try:
            await page.goto(
                job_summary.url,
                wait_until="domcontentloaded",
            )
            await page.wait_for_selector(".job-detail")
            await self.close_login_dialog_if_exists(page)
            detail = await page.locator(".job-sec-text:not(.fold-text)").inner_html()
            posted_date = await page.locator("p.gray").inner_text()
            job.posted_date = self.__get__job_posted_date(posted_date)
            job.detail = detail
            job.boss = Boss()
            job.boss.title = self.__get__boss_title(
                await page.locator(".job-boss-info .boss-info-attr").inner_text()
            )
            job.boss.name = self.__get__boss_name(
                await page.locator(".job-boss-info .name").inner_text()
            )
            job.boss.active_state = await page.locator(
                ".job-boss-info .boss-active-time"
            ).inner_text()
            return job
        except Exception as e:
            print(f"get job:{job_summary.id} failed,detail:{e}")
            return job
        finally:
            sleep_time = random.randint(1, 10)
            await asyncio.sleep(sleep_time)
            await page.close()

    def __get__job_id(self, job_url):
        parsed_url = urlparse(job_url)
        path = parsed_url.path.split("/")[-1].split("?")[0]
        job_id = path.split(".")[0]
        return job_id

    def __get__boss_title(self, title):
        parts = title.split("\n")[-1]
        return parts

    def __get__boss_name(self, name):
        result = name.split("\n")[0]
        return result

    def __get__job_posted_date(self, posted_date):
        date_part = posted_date.split("：")[1]
        return date_part
