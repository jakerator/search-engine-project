# Web Search Engine System
(Django + Celery + Postgres + OpenSearch + S3 + Redis)

A scalable web search engine featuring:

- Distributed crawling (with **1-hour SLA**)
- Link extraction & recursive crawling
- Raw content Blob storage in S3
- OpenSearch indexing (AWS ElasticSearch)
- Keyword search API
- Page Details API
- Scalable infrastructure (multiple api instances, workers, db clustering)


![System Architecture](./docs/architecture.svg)
([View full diagram](https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=search-system.drawio&dark=auto#R%3Cmxfile%3E%3Cdiagram%20name%3D%22Page-1%22%20id%3D%22dTkWM2QsZdfghEIHy5cy%22%3E7V1bc5u6Fv41nul5aAaJm%2F2Y2L1OOju76czuedojg2zTYOSCSOL%2B%2BiOBZBuQHYIl23NCHpKwjDDo%2B5bW0qcLA3u8fP6UotXiGwlxPIBW%2BDywJwMIoeV57A%2B3rEsLALZfWuZpFArb1nAf%2FcHCaAlrHoU4q5xICYlptKoaA5IkOKAVG0pT8lQ9bUbi6reu0Bw3DPcBipvWf6KQLkrr0LW29s84mi%2FkNwNLfLJE8mRhyBYoJE87JvvDwB6nhNDyv%2BXzGMe89mS9lOU%2B7vl0c2MpTmibAunHxYfbhf1%2B%2BjOfgj%2Bj2Z0Pp%2B8VVxGmjK5lHWRP0TJGCTu6mZGE3otPADtGcTRP2P8BK45TZnjEKY1Y9V2LDyhZMWuwiOLwFq1Jzr8koyh4kEc3C5JGf9hlUSyuyT5OqWCCDypn3POSzGwxa4ozds6dvHNQM31Dz5UTb1FGhSEgcYxWWTQtHoNbliidR8kNoZQshamshUcU56IWBtCLafFB%2BRc%2FsydO2F1Dby7s8u8A2oBfYxxH%2FObKK7GKwc87VSxQ%2BoTJEtN0zU5Z7BIJCs952rIO2AKbjXuVh8K3HOAI3gvOzzeX3tKC%2FSOY8QqWwCZLDrFphzpxVNAmoyl52DgQh2oWxfGYxIRxZpKQ4iTJpRjPqIJJyygM4%2BJiKxREyfwHZ9bkPdhabouCE3tr%2BS4qlJtSQhFFW8xjNMXxHckiGhF%2B%2FbQ892ZFooQWNejeDNxJYUnpmCTsIVBUPD9mXHrCnE%2FiyeSTRMkCpxHd0ud1oA%2F3Qy4w9oEhiO3OELMHbFaEgPT1KJftRRVQpwkoNxFWdhYXTeqCcQMnCpCrYN4whxlbVy6HFY7ZMdgev4i0okG4YTceX6%2Bid%2F%2FpBLfjv4z3yBDezoU3%2FO7ZGv5dzrKGHIPQxX6D4OyTkefbyGsTKia%2FUDInBwJFecL13ZdOPGItf4NIjDrVWOFVg4XtmmKW27IlcfpgcVSwcKz9oAuQXVPRwuuM8VuOFguUMFKOU%2FQUf8e%2Fc3Zix8Bhvwz9yBT0fg%2F9cdCzUEbzzBzyAJqCfthD3xn6e4zSYGEQdWNt%2FahHvTPqd2iOJ5iiKDbp8ENjYb6P892x%2F7FgX0tjbA54CEwBD6wm8BfVPfTgFXQvpIcIpghgKCphxz4rflQ9R8vyPlx%2FbNNzzHD6GAX4kMZY5BTytC5KY1mXTbLBSgfSk1KEbHV8yxT5FKL0QZb2XUidXUhYgXmHHPqBbq0rN4F%2By%2FEly6fLiBaO%2Fy5PY43xpYo9sEyC31px7sHfBX%2BO6VcyFZ3IX2T6JTSHv20S%2F0tXoM839HhR%2BUXZcT0qwVDI02DoHMwuPMtYdtFWnwa9QK09u9jAbno4E7TtuSpQfsvRJStlqt85Ttfa4koddWCu36pQp%2FugcnlBhetiukMKdA53WB1zIaWtMC7p2YcUjR1WCbvxkNJWCFeg%2FJZDCuuw7MrgfMakzj5LDX5zsQVeuibq%2BFfe7o9%2FIaEmRHg4C1QhxQuGeDprE1KeSPrA6uyADIpjXPClkEX4qR34BUfVKmzOz4KuVwkywLer82pcCK5kOf0UbKuMwl4Z1R9oJPQyn2i4myHQ26qkCtDfctwJeEPAIw%2FXSPkloRXiFV3oCz01QgxPRYi2ymlPiAohZpiyrq1WwbzGAABORQGFeNpT4GUKsEdPUUBvo%2BQhe7egS4NUqIcHU9NtYVs9s6dChQqsvjJ8nYTjGKPEMBf8U3GhrerZc6GqelKS4u%2FoySwNoHUqGrSdo9vToEmDO94uhO%2BK5kGjTFHngn0qLrTVJnsuVLgQJSF%2BnpAgX7JqM84GT6k76CeDQsK8KAnLG55Ls0pJzhAPB01NpBwUgYFSwQq9qee2WgP2HYdRdkDAKj6%2F4Zfvpl0BW7F61BVdRXkZp7YKDAzhlZyIo39JqUIwPUjLvukpmh6Ksoe%2Fc5x3GxpTjb9KGsjJFUNTiLfWJ5uI9%2FrksXMraiiPjKGsECQvK4pYlxFFZBXcFtQuTPMYZdlAOUyiI8iEnLcoOzj0TjI6Z0836UY84CmY51QncwEIqgsVbMsYF9tqoZK0fYwR6sccZ9rii1Od3yMpoh%2FttrJnj3ZzKOQrmRpDfGQM8bbqpgLxPqM4NqOooQygMZgVwmWfUrRLKQykEdOYTP%2FlahjfHO3A1HD7Jg8ecMcNrhSJxGZHnH2JhAuMMbCtZiqp2oeWIrSwyPKZLuO%2Fpr9wQLXFlw0RjGcUbeXRHvbm6FnISlBWbYbBN5dctJ3RqQC%2FTy6Onrdb37bEFMyOQoe8rOTibKr3Zk%2FSk0jg5eKSf4uhlQNpxV8rnJSrzsZxntGuerin0MOHNT28nl%2F4xvILp6006vTjcA2h4kvJGE191%2BGJ1HCv9U54PeQNyMsGwBTmxrRxuRqhC%2BZ9SnH06tIqygAag1l8EQ4bu4c3cwySpwE%2BcLFmLhLk6eO2y88zhWu%2BlfkWfpyE0kJWhY%2Fi54j%2BFCX4%2F%2F%2FlyF25xbnsiX8KIIuD7WfbkG818AnxDOXxFh92G3N8kNINZ%2F7848cds6TlZoeZGtQUx4hGj9V6VCFWFGWPjdY7JwgG1gHdXP8IjB2NGDdXGR%2BBsXU1GnkVnAGAr0Kal5w87x6sdw7umF%2By2uOpbmljNSDzYebeCzInCYo%2FbK1tGSKzqx2KFNL0gOf%2BN0X98G0tjuTJcZ7takTda%2FYbz%2BTaBwDXBm7T%2F7NNED8bnN6lOvFRaGrDzG9gVrwQgy%2BVKZZrnhU7X2eQbY4PaQWvtbvtARluGLAtVxxp91M5Urbrp%2BiRY%2F6LTHWE6OXzHQ%2FKlW52ffPxWje7vGlRzEAoH%2BpkUjNz18YkGx4bqrvSqyV55MStHfLg5Hc5Wc2SsZxPYDsNkUZ1vcY0kUY6iWQwnrAbfYEMNZadouVxmunfA14%2FkTTktXD2XEE2SnrAbW4Cca5k4SRBxW5AGxMUDsQLtqDFIEJ8dtpZAQY6AW5OYT0JwPY5cns5ANaElzX5DItyOHBQvIaNildenQ1lndoM1NNGSyyB4YZ4v0LA93Z8bTLRPSfQEf33Kz3q5ABaTjU58Hxvl0wvF5CjQVv2lfewp%2FjmVX8yq7VryUjJrkYy0kxrPMu6sixQu5kRB9Ha%2FNRe7mY403F1ql9yx4LTeZH0g4oPDB2nW0JtPHo2m9diLaJsX4U6JltZE5m169ecp75b2h4ya%2BObTt0NatHd2lBqNBx176OBKwt4tei%2BFXL3kY4fGVNoFSm6GK63SMp%2B5SuWxOFzNO%2FAr78aT7zBbG%2Br2ijgWYcLuK51bAH4igACvNreUcP6TKfWAcSphSL%2FxAKLq1NmVaxEPmPOtcmottGjvBAP2GcbSVGIeNI1Nfe4ujnryKmucJaK335nddQSYfsCQuTr6Hu%2BXRsrNhzvPJ3idrOTUiX4lmq3pJgJwJn7C1O6FjPQUE4JM%2FHtLwbbzmizY1rKiC3EbeYdfi2y2UMzka3SNqjagfBjxLF5TZfGPksPxquFEwccjnD18%2B3XhR9Qe3%2B0XX%2Bji%2BGgISdeiVe3i%2BkmA6jaaPOgD%2B3wntPllk9WqbL5xRmcmwkzxTzKvXOdJgPFlKXydU%2FMdn97LT58eSqLkkmiCPOe4QhWsGmf0MtTyGyW4WNx%2BzS%2F%2B%2Frz%2FeNi%2FefvBf3yz0%2F843e6GQB5bdOlvpgSwsMef3TjpsO5m%2F5k1zZXcOT8cv3%2BpK5K0N6fDgJ7Zn8qduTKV8z4ijXKL%2FgTrOUj8pX2l%2BFQ%2B93nIuan%2Fz9vLJwFCxzm8eG9hVOSFCLMR%2FZ7s9HwFKOOK9%2F27BJZWXlpVRjc2GbYHmqYqK4kI2zbWDQY2s9fPXq9bS2A6N9NVAmlYg%2BFlpC%2F5WnqQRmm%2FopDvrL%2BXYjWmb43ptSYcPzWwuwwJYTuBq4UrRbfSMhj%2B4f%2FAQ%3D%3D%3C%2Fdiagram%3E%3C%2Fmxfile%3E))




---

## 🗂 Repository Structure

```text

├─ requirements.txt            # Django, Celery, Redis, OpenSearch, boto3, etc.
├─ env.example                 # Environment template

├─ app/                        # Django project configuration
│  ├─ settings.py
│  └─ urls.py

├─ api/                        # HTTP layer (controllers)
│  ├─ views.py                 # /crawl, /crawl/{job_id}, /search, /pages/{id}
│  └─ throttling.py            # SLA-aware throttling (overload protection)

├─ services/                   # Business logic
│  ├─ crawl_service.py         # submitCrawl(), getJobStatus()
│  ├─ search_service.py        # OpenSearch query pipeline
│  └─ page_service.py          # Page metadata (Postgres) + content (S3)

├─ tasks/                      # Tasks (Celery)
│  ├─ crawl.py                 # crawlPage(job_id, url, max_depth, max_pages)

├─ models/                     # Models
│  └─ crawl_job.py             # CrawlJob (Crawl job tree + SLA fields)
│  └─ page.py                  # Page (Metadata for each crawled page) models

├─ integrations/               # External system adapters
│  ├─ index_client.py          # OpenSearch adapter
│  ├─ blob_storage_client.py   # S3 adapter
│  ├─ http_client.py           # fetch HTML (headless browser/service)

```


## 🔧 Key Components

Below is an overview of all major components in the system and how they interact.

---

### **1. API Layer (`api/`)**
The HTTP interface exposed to external clients.

**Responsibilities:**
- Handle incoming REST requests
- Handle Auth if needed
- Validate input, apply throttling, return responses
- Delegate business logic to services

**Endpoints:**
- `POST /crawl` – Submit crawl or re-crawl job
- `GET /crawl/{job_id}` – Retrieve job status
- `GET /search` – Search indexed pages
- `GET /pages/{page_id}` – Retrieve full page metadata + stored content

**Key Files:**
- `views.py` – Request handlers

---

### **2. Services Layer (`services/`)**
Contains business logic independent from HTTP and workers.

#### **CrawlService**
- Creates crawl jobs
- Enforces 1-hour SLA logic (before creating job)
- Pushes crawl tasks to Redis/Celery
- Get job status from SQL DB

#### **SearchService**
- Handles keyword searches
- Sends queries to OpenSearch
- Returns titles, snippets, scores, URLs, page IDs

#### **PageService**
- Loads page metadata (from SQL DB)
- Fetches raw/parsed content from Blob storage (S3)

---

### **3. Crawler System (`crawler/`)**
Distributed crawling engine run by Celery workers.

**Responsibilities:**
- Fetch HTML
- Extract links from HTML content
- Maintain single Browser session (Chrome headless)
- Parse + clean content
- Store raw in Blob Storage (S3)
- Save pages metadata to SQL DB
- Index cleaned text in OpenSearch
- Handle SLA requirement during crawling

**Key Files:**
- `crawl.py` – Main crawl pipeline (`run_crawl_job`)
- `models/pages.py` – Page metadata
- `models/crawl_jobs.py` – CrawlJob

---

### **4. Integrations (`integrations/`)**
Unified adapters for external systems.

#### **Index Client (OpenSearch) **
- Index new documents
- Update existing pages
- Execute search queries

#### **Blob Storage Client**
- Upload raw HTML & parsed content
- Retrieve page content for PageService

#### **HTTP Client**
- Scraping urls with Headless Browser (Playwrite)

---

### **5. Storage Layer**
Not folders, but critical components:

#### **Postgres**
- Stores `pages` table
- Stores `crawl_jobs` (root + recursive jobs)
- Tracks crawl status, SLA deadlines, metadata

#### **S3**
- Raw HTML (compressed)

#### **OpenSearch**
- Full-text search index
- Stores searchable content, title, snippet, metadata

---

This modular layout ensures clear separation of concerns between:
- **HTTP handlers**
- **Business logic**
- **Crawler pipeline**
- **External system adapters**
- **Data storage**




---
## 🚀 Run locally

From the project root ([manage.py](http://_vscodecontentref_/3) directory):

```bash
# 1. Create and activate a virtualenv (optional if already using one)
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run database migrations (uses default SQLite in `app/settings.py`)
python manage.py migrate

# 4. Install Playwrite (headless browser for scraping html)
playwright install

# 5. Start the Django development server
python manage.py runserver