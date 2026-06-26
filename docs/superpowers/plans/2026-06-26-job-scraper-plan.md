# Data Job Scraper Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Scrapy project that scrapes Wellfound for AI/Data job listings and exports to CSV/JSON.

**Architecture:** Single Scrapy project with one spider (`wellfound.py`), one item model (`JobItem` in `items.py`), and two pipelines (cleaning + deduplication in `pipelines.py`). Output via Scrapy's built-in feed exporters.

**Tech Stack:** Python 3.10+, Scrapy 2.11+

## Global Constraints

- Use Scrapy's built-in CSV and JSON feed exporters (no custom export code)
- Spider must accept a `role` parameter for search term
- Output files: `jobs.csv`, `jobs.json`

---

### Task 1: Scaffold the Scrapy project

**Files:**
- Create: `job_scraper/` (via `scrapy startproject`)

**Interfaces:**
- Consumes: nothing
- Produces: Scrapy project skeleton with `items.py`, `pipelines.py`, `settings.py`, `spiders/` directory

- [ ] **Step 1: Install Scrapy**

```bash
pip install scrapy
```

- [ ] **Step 2: Generate the project**

```bash
cd /Users/almas/Desktop/opencode/data_job_scraping
scrapy startproject job_scraper .
```

Expected: Creates `job_scraper/`, `scrapy.cfg`, and default files.

- [ ] **Step 3: Verify it works**

```bash
scrapy list
```

Expected: No spiders listed (empty list).

---

### Task 2: Define the JobItem model

**Files:**
- Modify: `job_scraper/items.py`

**Interfaces:**
- Consumes: nothing
- Produces: `JobItem(title, company, remote, location, salary_range, description, posted_date, role_type, url)`

- [ ] **Step 1: Replace `items.py` content**

```python
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
```

- [ ] **Step 2: Verify import works**

```bash
python -c "from job_scraper.items import JobItem; print('OK')"
```

Expected: `OK`

---

### Task 3: Write the Wellfound spider

**Files:**
- Create: `job_scraper/spiders/wellfound.py`

**Interfaces:**
- Consumes: `JobItem` from `job_scraper.items`
- Produces: Yields `JobItem` instances for each job listing

- [ ] **Step 1: Create `wellfound.py`**

```python
import scrapy
from ..items import JobItem


class WellfoundSpider(scrapy.Spider):
    name = "wellfound"

    def __init__(self, role="Data Engineer", **kwargs):
        super().__init__(**kwargs)
        self.role = role

    def start_requests(self):
        url = f"https://wellfound.com/jobs?q={self.role.replace(' ', '+')}"
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        jobs = response.css("div.job-listing")
        for job in jobs:
            item = JobItem()
            item["title"] = job.css("h2::text").get("").strip()
            item["company"] = job.css("span.company::text").get("").strip()
            item["remote"] = job.css("span.remote::text").get("").strip()
            item["location"] = job.css("span.location::text").get("").strip()
            item["salary_range"] = job.css("span.salary::text").get("").strip()
            item["description"] = job.css("div.description::text").get("").strip()
            item["posted_date"] = job.css("time::attr(datetime)").get("").strip()
            item["role_type"] = self.role
            item["url"] = response.url
            yield item

        next_page = response.css("a.next-page::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

- [ ] **Step 2: Verify spider loads**

```bash
scrapy list
```

Expected: `wellfound`

---

### Task 4: Write the pipelines

**Files:**
- Modify: `job_scraper/pipelines.py`

**Interfaces:**
- Consumes: `JobItem` from the spider
- Produces: Cleaned + deduplicated `JobItem`

- [ ] **Step 1: Replace `pipelines.py` content**

```python
import hashlib
import scrapy


class CleanPipeline:
    def process_item(self, item, spider):
        for field in item.fields:
            if item.get(field):
                item[field] = item[field].strip()
        return item


class DedupPipeline:
    seen = set()

    def process_item(self, item, spider):
        fingerprint = hashlib.md5(
            f"{item.get('title', '')}{item.get('company', '')}{item.get('url', '')}".encode()
        ).hexdigest()
        if fingerprint in self.seen:
            raise scrapy.exceptions.DropItem(f"Duplicate: {item}")
        self.seen.add(fingerprint)
        return item
```

- [ ] **Step 2: Verify pipelines import**

```bash
python -c "from job_scraper.pipelines import CleanPipeline, DedupPipeline; print('OK')"
```

Expected: `OK`

---

### Task 5: Configure settings

**Files:**
- Modify: `job_scraper/settings.py`

**Interfaces:**
- Consumes: Nothing new
- Produces: Enabled pipelines, feed export config

- [ ] **Step 1: Add pipeline and feed config to `settings.py`**

Add at the end of `settings.py`:

```python
ITEM_PIPELINES = {
    "job_scraper.pipelines.CleanPipeline": 200,
    "job_scraper.pipelines.DedupPipeline": 300,
}

FEEDS = {
    "jobs.csv": {"format": "csv", "overwrite": True},
    "jobs.json": {"format": "jsonlines", "overwrite": True},
}

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"

DOWNLOAD_DELAY = 1.0
```

- [ ] **Step 2: Verify config loads**

```bash
python -c "from scrapy.utils.project import get_project_settings; s = get_project_settings(); print(s.get('ITEM_PIPELINES'))"
```

Expected: Shows the pipeline dict.

---

### Task 6: Run and verify end-to-end

**Files:** None

- [ ] **Step 1: Run the spider with a test role**

```bash
scrapy crawl wellfound -a role="Data Engineer" -o jobs.csv -o jobs.json
```

Expected: Spider runs, crawls Wellfound, outputs items.

- [ ] **Step 2: Check CSV output**

```bash
head -5 jobs.csv
```

Expected: CSV with headers and at least one row of data.

- [ ] **Step 3: Check JSON output**

```bash
head -5 jobs.json
```

Expected: JSON lines with job data.

- [ ] **Step 4: Commit the project**

```bash
git init && git add -A && git commit -m "feat: initial scrapy project for wellfound job scraping"
```
