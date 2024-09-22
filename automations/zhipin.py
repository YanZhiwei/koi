import random
from typing import List
from urllib.parse import urlparse

from playwright.sync_api import Page, sync_playwright

from chrome import get_chrome_path_windows
from models.boss import Boss
from models.job import Job
from models.job_summary import JobSummary


class Zhipin(object):

    def __init__(self, city: str):
        self.url = "https://www.zhipin.com/"
        self.city = city
        self.browser = None
        self.context = None

    def __del__(self):
        self.browser.close()

    def __instance_browser(self):
        chrome_path = get_chrome_path_windows()
        if chrome_path is None:
            raise Exception("chrome path not found")
        p = sync_playwright().start()
        self.browser = p.chromium.launch(
            executable_path=chrome_path,
            headless=False,
            args=["--disable-infobars", "--start-maximized"],
            ignore_default_args=["--enable-automation"],
        )
        self.context = self.browser.new_context(no_viewport=True)

    def close_login_dialog_if_exists(self, page: Page):
        try:
            if page.locator(".boss-login-dialog").is_visible():
                page.locator(".boss-login-close").click()
        except Exception as e:
            print(e)

    def search(self, keyword: str) -> List[JobSummary]:
        job_summarys: List[JobSummary] = []
        if not self.browser:
            self.__instance_browser()
        page = self.context.new_page()
        page.goto(
            "https://www.zhipin.com/shanghai/?seoRefer=index",
            wait_until="domcontentloaded",
        )
        page.type('[name="query"]', keyword)
        page.click(".btn-search")
        page.wait_for_selector(".job-list-box")
        search_url = page.url
        for i in range(1, 11):
            search_page_url = search_url + f"&page={i}"
            page.goto(search_page_url, wait_until="domcontentloaded")
            page.wait_for_selector(".job-list-box")
            page.wait_for_selector(".job-list-box > li")
            self.close_login_dialog_if_exists(page)
            job_result = page.locator(".job-list-box > li").all()
            for job in job_result:
                job_name = job.locator(".job-name").inner_text()
                job_area = job.locator(".job-area").inner_text()
                job_link = job.locator(".job-card-left").get_attribute("href")
                company_name = job.locator(".company-name").inner_text()
                info_desc = job.locator(".info-desc").inner_text()
                tag_list = job.locator(".tag-list > li").all()
                tags = [tag.inner_text() for tag in tag_list]
                job_summary = JobSummary()
                job_summary.name = job_name
                job_summary.language = keyword
                job_summary.area = job_area
                job_summary.url = f"https://www.zhipin.com{job_link}"
                job_summary.company = company_name
                job_summary.salary = job.locator(".salary").inner_text()
                job_summary.tags = tags
                job_summary.description = info_desc
                job_summary.id = self.__get__job_id(job_summary.url)
                job_summarys.append(job_summary)
        return job_summarys

    def get_job(self, job_summary: JobSummary) -> Job:
        job: Job = Job()
        job.summary = job_summary
        job.id = job_summary.id
        if not self.browser:
            self.__instance_browser()
        page = self.context.new_page()

        try:
            page.goto(job_summary.url, wait_until="domcontentloaded")
            page.wait_for_selector(".job-detail")
            self.close_login_dialog_if_exists(page)
            detail = page.locator(".job-sec-text:not(.fold-text)").inner_html()
            posted_date = page.locator("p.gray", has_text="更新于").inner_text()
            job.posted_date = self.__get__job_posted_date(posted_date)
            job.detail = detail
            job.boss = Boss()
            job.boss.title = self.__get__boss_title(
                page.locator(".job-boss-info .boss-info-attr").inner_text()
            )
            job.boss.name = self.__get__boss_name(
                page.locator(".job-boss-info .name").inner_text()
            )
            job.boss.active_state = page.locator(
                ".job-boss-info .boss-active-time"
            ).inner_text()
            return job
        except Exception as e:
            print(f"get job:{job_summary.id} failed, detail:{e}")
            return job
        finally:
            sleep_time = random.randint(1, 10)
            page.wait_for_timeout(sleep_time * 1000)  # Convert to milliseconds
            page.close()

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
