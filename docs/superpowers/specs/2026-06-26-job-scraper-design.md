# Data Job Scraper — Design Doc

## Purpose

Scrape job listings from RemoteOK's RSS feed for AI/Data roles (AI Engineer, Data Engineer, AI Developer, Data Analyst) as a project to learn Scrapy fundamentals.

## Architecture

Standard Scrapy project with one spider, one item model, and a cleaning+d duplication pipeline.

```
data-job-scraper/
├── scrapy.cfg
├── agents.md
├── jobs.csv              # output (auto-generated)
├── jobs.json             # output (auto-generated)
└── job_scraper/
    ├── __init__.py
    ├── items.py           # JobItem schema
    ├── middlewares.py      # default
    ├── pipelines.py       # CleanPipeline + DedupPipeline
    ├── settings.py        # config
    └── spiders/
        └── wellfound.py   # RemoteOK spider (named "remoteok")
```

## Components

### Spider (`spiders/wellfound.py` — spider name: `remoteok`)

- Fetches RemoteOK's RSS feed: `https://remoteok.com/remote-jobs.rss` (all jobs) or `https://remoteok.com/remote-{role}-jobs.rss` (filtered)
- Parses RSS XML with Scrapy XPath selectors
- Accepts a `role` parameter for search filtering
- Yields `JobItem` for each job

### Items (`items.py`)

```python
class JobItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    remote = scrapy.Field()        # Always "Yes" on RemoteOK
    location = scrapy.Field()
    salary_range = scrapy.Field()  # Not always available on RemoteOK
    description = scrapy.Field()
    posted_date = scrapy.Field()   # RFC 822 date from RSS
    role_type = scrapy.Field()     # Which role search found this
    url = scrapy.Field()
```

### Pipelines (`pipelines.py`)

- **CleanPipeline**: trim whitespace on all string fields
- **DedupPipeline**: skip jobs already seen (by title + company + URL fingerprint)

### Export

Run via:
```bash
scrapy crawl remoteok -a role="Data Engineer" -o jobs.csv -o jobs.json
```

Scrapy's built-in CSV and JSON lines exporters handle output.

## Data Flow

```
Spider fetches RSS XML → parses with XPath → yields JobItem
    → CleanPipeline trims fields
    → DedupPipeline removes duplicates
    → CSV + JSON files
```

## Key Learning Points

- **Spiders**: how to write a spider that makes requests and parses responses
- **XPath selectors**: navigating XML/HTML structure
- **Items**: defining data schemas with scrapy.Field
- **Pipelines**: processing items (clean + deduplicate)
- **Settings**: configuring feeds, pipeline order, delays
- **Real-world challenge**: some sites (Wellfound) need advanced techniques like Playwright to bypass anti-bot protection

## Future Enhancements

- Add more spiders for other job boards (LinkedIn, Indeed, Wellfound with Playwright)
- Store in SQLite database
- Schedule regular runs with cron
