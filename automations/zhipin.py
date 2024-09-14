from typing import List

from clicknium import clicknium as cc
from clicknium import locator
from clicknium.core.models.web.browsertab import BrowserTab

from models.job import Job
from models.job_summary import JobSummary


class Zhipin(object):

    def __init__(
        self,
        city: str,
    ):
        self.url = "https://www.zhipin.com/"
        self.city = city
        self.tab: BrowserTab = None

    def __del__(self):
        if self.tab is not None:
            self.tab.close()

    def __instance_browser(self) -> BrowserTab:
        tab = cc.chrome.open(
            "https://www.zhipin.com/",
            args=["--disable-infobars"],
        )
        return tab

    def search(self, keyword: str) -> List[JobSummary]:
        jobSummarys: List[JobSummary] = []
        # if not self.tab:
        #     self.tab = self.__instance_browser()
        # self.tab.find_element(locator.zhipin.input_search).set_text(keyword)
        # self.tab.find_element(locator.zhipin.btn_search).click()
        search_tab = cc.chrome.attach_by_title_url(
            url=f"https://www.zhipin.com/web/geek/job*"
        )
        print(search_tab.url)
        result = search_tab.scrape_data(
            locator.zhipin.search_result,
            next_page_button_locator=locator.zhipin.btn_page_next,
        )
        print(result)
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
