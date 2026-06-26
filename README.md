# Data Job Scraper

Scrape job listings from RemoteOK for AI/Data roles using Scrapy. Built to learn web scraping fundamentals.

## Features

- Scrapes RemoteOK RSS feed for job listings
- Filter by role: Data Engineer, AI Engineer, Data Analyst, AI Developer
- Clean and deduplicate pipelines
- Export to CSV and JSON

## Setup

```bash
pip install scrapy
```

## Usage

```bash
# All jobs
scrapy crawl remoteok -o jobs.csv -o jobs.json

# Filter by role
scrapy crawl remoteok -a role="Data Engineer" -o jobs.csv
scrapy crawl remoteok -a role="AI Engineer" -o jobs.csv
scrapy crawl remoteok -a role="Data Analyst" -o jobs.csv
scrapy crawl remoteok -a role="AI Developer" -o jobs.csv
```

## Project Structure

```
├── scrapy.cfg
├── job_scraper/
│   ├── items.py           # JobItem schema
│   ├── pipelines.py       # Clean + dedup pipelines
│   ├── settings.py        # Config (feeds, delays, user-agent)
│   └── spiders/
│       └── wellfound.py   # Spider (name: remoteok)
```

## What I Learned

- Spiders, XPath selectors, Items, Pipelines, Settings
- Real-world anti-bot protection (Wellfound blocks with Cloudflare)
- RSS feed parsing as an accessible alternative
- Playwright integration for JavaScript-rendered sites
