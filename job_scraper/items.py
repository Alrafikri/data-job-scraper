import scrapy


class JobItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    remote = scrapy.Field()
    location = scrapy.Field()
    salary_range = scrapy.Field()
    description = scrapy.Field()
    posted_date = scrapy.Field()
    role_type = scrapy.Field()
    url = scrapy.Field()
