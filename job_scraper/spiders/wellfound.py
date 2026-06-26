import scrapy
from ..items import JobItem


class RemoteOKSpider(scrapy.Spider):
    name = "remoteok"

    def __init__(self, role="", **kwargs):
        super().__init__(**kwargs)
        self.role = role

    def start_requests(self):
        if self.role:
            url = f"https://remoteok.com/remote-{self.role.replace(' ', '-').lower()}-jobs.rss"
        else:
            url = "https://remoteok.com/remote-jobs.rss"
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for item in response.xpath("//item"):
            job = JobItem()
            job["title"] = item.xpath("title/text()").get("").strip()
            job["company"] = item.xpath("company/text()").get("").strip()
            job["description"] = item.xpath("description/text()").get("").strip()
            job["location"] = item.xpath("location/text()").get("").strip()
            job["posted_date"] = item.xpath("pubDate/text()").get("").strip()
            job["url"] = item.xpath("link/text()").get("").strip()
            job["remote"] = "Yes"
            job["salary_range"] = ""
            job["role_type"] = self.role or "all"
            yield job
