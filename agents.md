# Data Job Scraping — Learning Scrapy

Learning scrapy with job board scraping related to:
- AI Engineer
- Data Engineer
- AI Developer
- Data Analyst

## Commands
- Run spider: `scrapy crawl remoteok -a role="Data Engineer" -o jobs.csv`
- Run all jobs: `scrapy crawl remoteok -o jobs.csv`
- Run with JSON too: `scrapy crawl remoteok -o jobs.csv -o jobs.json`
- `scrapy` binary at: `~/Library/Python/3.9/bin/scrapy` (add to PATH)

## What We Built

Standard Scrapy project scraping RemoteOK RSS feed.

### Files
- `job_scraper/items.py` — `JobItem` with 9 fields: title, company, remote, location, salary_range, description, posted_date, role_type, url
- `job_scraper/spiders/wellfound.py` — spider named `remoteok`, fetches RSS XML and parses with XPath
- `job_scraper/pipelines.py` — CleanPipeline (trims whitespace) + DedupPipeline (fingerprints by title+company+url)
- `job_scraper/settings.py` — feed export (CSV + JSON), pipeline order (200, 300), 3s delay, custom user-agent

### How It Works
1. Spider requests `https://remoteok.com/remote-{role}-jobs.rss` (or all jobs)
2. Scrapy returns parsed XML response
3. Spider uses XPath (`//item`, `title/text()`, etc.) to extract job fields
4. Each job is yielded as a `JobItem`
5. Pipelines clean and deduplicate
6. Scrapy writes to CSV + JSON

## Lessons Learned

| Lesson | Detail |
|--------|--------|
| **Spiders** | Define start URLs, parse responses, yield items |
| **XPath selectors** | Navigate XML/HTML with `response.xpath("//item/title/text()")` |
| **Items** | Blueprint for data with `scrapy.Field()` |
| **Pipelines** | Process items in sequence (clean → dedup) |
| **Settings** | Configure feeds, pipeline priority, delays |
| **Anti-bot protection** | Wellfound uses Cloudflare/DataDome — can't scrape with basic HTTP |
| **Fallback strategy** | RemoteOK RSS feed works with plain HTTP, good for learning |
| **Playwright** | `scrapy-playwright` + `playwright install chromium` for JS-heavy sites |

## Next Ideas
- Add spider for Wellfound using Playwright with stealth techniques
- Store jobs in SQLite database
- Parse salary from description text
- Schedule regular runs with cron
- Add more boards (LinkedIn, Indeed)
