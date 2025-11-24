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
([View full diagram](https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=Untitled%20Diagram.drawio&dark=auto#R%3Cmxfile%3E%3Cdiagram%20name%3D%22Page-1%22%20id%3D%22dTkWM2QsZdfghEIHy5cy%22%3E7V1dc6o6F%2F41zvRcbIeED%2FWy1e6v6Z7ds9uZ0%2FfqTIQotEjcENq6f%2F2bQCLyoaWaqHOKF60sCEKeJ1krDyuhZ44Xr19itPR%2FEA%2BHPWh4rz1z0oMQGo7D%2FnHLKrcAYA5yyzwOPGErDHfBHyyMhrCmgYeT0oGUkJAGy7LRJVGEXVqyoTgmL%2BXDZiQs%2F%2BoSzXHNcOeisG79J%2FCon1uHtlHYv%2BJg7stfBobYs0DyYGFIfOSRlw2Ted0zxzEhNP%2B2eB3jkNeerJe83Octe9cXFuOItikQf%2Favb3zz0%2FQhnYI%2Fo9ntAE4%2FNZxFmBK6knWQvASLEEVs62pGInon9gC2jcJgHrHvLiuOY2Z4xjENWPVdih2ULJnV9YPQu0ErkvIfSShyn%2BTWlU%2Fi4A87LQrFOdnumAomDEDpiDtekpkNZo1xwo65lVcOKqYf6LV04A1KqDC4JAzRMgmm2W1wywLF8yC6IpSShTDltfCMwlTUQg86Ic125P%2FxK7vjiF01dObCLv%2F3oAn4OcZhwC8uPxOrGPy6UcUCpS%2BYLDCNV%2BwQf5NIULScl4J1wBTYrJtXvinalgUswXvB%2Bfn61AUt2BfBjHewBNZZsotNG9QJg4w2CY3J07oBcahmQRiOSUgYZyYRyQ6SXArxjDYwaRF4XpidbIncIJrfc2ZNPoHCcpMVnJiF5ZeoUG6KCUUUFZiHaIrDW5IENCD8%2FHF%2B7NWSBBHNatC%2B6tmTzBLTMYnYTaAgu3%2FMuPSCOZ%2FEnck7CSIfxwEt6PM%2B0IfbIRcYD4AmiM29IWY3WK8IAen7Uc77izKgVh1QbiKs7CzMulSfcQNHDSCXwbxiDWZs9G0OKxyzbVBsv4l0Q4dwxS48vFwGF3%2FtBbc1eBvvkSa8rTPv%2BO2TdfybnGUdOQaejQc1grM9I2dgIqeNq5g8omhOdjiK%2FIDL22978Yj1%2FDUiMeqUfYVTdhamrYtZdsuexOqcxUHOwjK2gy5AtnV5C2dvjD%2Byt%2FBRxEkJjXGMXngd%2F8K%2FU374PvCbb8M%2F0gX%2FoINfBfzMqdE06Y1h79LQxQEAdZFg2JHgEBLcYRS7vjbYtXX9ow72Q2C%2F5XoTNCaYoiBMtME%2F1Ob5O9d%2FEP73Pvtlyr%2FqQR4CXcgDo478WQ0ZHdiH9pmMGsEUAQxFJWzYZ9mnaTRpGM715ec2o8kEx8%2BBi3fpjjzAuJOH7aM%2B5nVZJxssDSodKU%2FIbmdg6CJfg1C9k6XdsFLlsBKWYN4gh3qgW2vNdaA%2FsoNJ0umCgS4HF4rHFGX8gaGTAK2V6I4AmwSYY47%2BdzItBpbQuHgk02%2Fefup0GyKYOolw7hL16Z5NnlWwkQ9kD4o2GvRrMLR2hhqOoS3UaCtgg07BVh5qrGHX%2FbwTtB3HNqD8kd1MImQr4%2BJ3iuOVMtdSBR7oG8c2qNedXzk%2Fv8KVMtVeBVq7B7CWPq%2FSVi6X9Oy8isIBrIRdu1dpq443oPyRvUo%2BeKlq48YFT69UOX6p8ECfk4HnLpZag76z%2BRmcic%2FxEB7O3Cbf4rhDPJ218S0vJH5idbZDH8UhzviSiSX80D34xZxHv1yDNbrZTsnbgIHkpMzPgKAvy6mnYFvJFHaSqXqPI6GXgUWtuWkCva182gD6R3ZALu8IuP%2B5SOOQnxIaHl5SX53rqRBieCxCtJVTO0KUCDHD1PU5GbQxAIBjUaBBSO0o8DYF2K3HyKU3QfSUXPh0oZEKVfegKzcXttU2OyqUqMDqK8GXkTcOMYo0c2FwLC60VUA7LpQVUEpi%2FAu96KUBNI5Fg7bCVEeDEg2CyMOvE%2BKmC1ZtF1kHoVCoqLLBPBYbGgSss9ItnOGphIqYpAxyr1cfCOeSOHQbZQvPmTp2q1lCv7AXJDtUi2z%2FFT%2F9foIFMBvmF9pifCBPY1XmCYEh7MuUDPWTDhtUsp207PqerO%2BhKHn6O8WpsizSNQ3k0%2FWhLsRbi1J1xDtR6tCH6xWUR9pQblChzsuLGOfhRWQV3GTUzkzzECVJr1EbV%2BFkPM5blOx88EoSOmd3N9mPeMBpYJ5VzuYBEJTT1k1DGxfbCmCStJ2PEUPeOVY2P2WN%2Fzp7SxfabbWuDu26%2Fv2dTLUhPtKGeFtJqwHxLqI4NKKooAygNpgb1KoupGgXUmgII6Yhmf7LlbAsZWN7brB5lbpPeM8lkBozOMrLWtQCCRtoY2DbWe%2BSqp1ryVwL8yxf6SL8OX3ELlU349Uq464vomib0tUAe%2BdfDk7cq6xooQtlq0GJOi%2F3cjLdc71u4VFE0Dy%2F%2FN9MXd%2FhWH4ucZRPPBmHaUL3VUSdBkV0WFFEqx7GGWojYVtxzOoexdSGqt9yxigavQyPpIc6rVfL6iCvQa52CZUq5trUUZmEvA%2FmXURx8ASzMsoAaoNZ%2FBD2aisM12MMksYu3nGyeizipvFzMejjkcIlX%2B64gB9HnrSQZdZG8WtAH0QJ%2Fv1%2FHLm%2BnR3L7vhBAJltFPsKl2%2FU8PHwDKVhgQ%2B7DJ7Kv6NSao356%2F39LbPE%2BVJoSTOoMQ4RDZ7L9diEWFaU3TZabRwgGFgFdH3%2BAzC2FGJcn2h4AMZGfzRySjgDAN%2BFNC85ed3cWG1s3LJ2yWqPh7q5jdWAjIdZ8%2FbJnEQovC6sbRkix%2B8bFHHFemms38%2FqJ5%2FcfhBPDmvZtkLUnfqw8URNewfgysCtt%2F9k7cRPBqdzro34IDSVYTaoYbbMJ2p5xSJmJ8NuoNLJ1p8QKAWvdXPbAjJcM6Aol20pb6fyWckG5sXChTeX%2BQSJBD3z7Ue%2B5MjhTnvxesvddGngXV2yuDLwzm9DFNPg3IcquVWP5ZVxy4SHOu99CdeSTjKZZ4NOOPqdJzAZ0rvzpKbjEGlUfUagm0gjlUTS6GHYhb5BhgrLjtEXWfWA8AmvXkjs8Vo4efQgOyU14NanhZ8qfDiKmzFr0IYEeT3xWh5oMIgQz1g6KcBAJcD1tMajAGyeItqXT8Tq8LIun2GRJ833spc3UfGinJOhrFKtgWr6aIkl0NwRb9cM%2BIJv7w0m9o8JVHj%2F7dpPc3AADascHDgDZ5NMbxeQz4cK9uXXsKX4%2BgVhMqo1K8FIzq5aMFIPaxzD6BsGqFzMiINorD%2BVV0JpjnRslXqYnLp8vFYk20GpDQwta7%2BAWrv3rHev2dw02b8KvUz2sjoia3tQaTzV9ZO2kFkZ31QqcVCJEteGUqPhaP8xGugbwKl490La3UY6vqVNs20I0cUDfIPE7E%2B6ZEEcPkX3DgbVF2qJ9x5t7VVrBRxjdwHbNg4tAN%2FhQIBTWURmWE2Kae1ArIorGhxZYLFVCq8N01NPGHOtI6rCe%2BQn4g77ZM9WGmQ92TQVj7j2a6wjqzztVSp%2B2xur1SwRti8gRL49297ArDw9Vufvvsxvvz98evZXf%2F726bd%2FHvD973itIr63xTSfrNZg3iZauQkUx9yQLHuAc%2FsRU7oSWWsopYSZ%2BEx5sVdPHGJWZq1aMmtTfU%2FWXJXiksVbiEVWRA82LQO3E9gKGDc8p6JcgW8mGq7zOrJ0v60pOZNeQ2ZNtr5FumTGd0z%2BagRPFGEdHqw0avk22RbwykPIbJZgPcBtbz5nkfb5X16mL3F97KXh7pX6YhJlI5nP7O962b4pRntOKdiy5lJpSotRYnBt0T5TRf5nIxlh286ixtAuLezgiUwVB6J%2Bba5GKBsmp7aE%2FCNnf7q5m%2FoZenzK4oWHVom6hcgrTDh8oT62GRNCNx1XjJb%2BD%2BJx3379fw%3D%3D%3C%2Fdiagram%3E%3C%2Fmxfile%3E))




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

├─ services/                   # Business logic
│  ├─ crawl_service.py         # submitCrawl(), getJobStatus()
│  ├─ search_service.py        # OpenSearch query pipeline
│  └─ page_service.py          # Page metadata (Postgres) + content (S3)

├─ tasks/                      # Tasks (Celery, Crons)
│  ├─ management
│  │  └─ commands
│  │     └─ cleanup_jobs.py    # Cleanup old jobs command (Cron/Celery Beat)
│  └─ crawl.py                 # run_crawl_job (Celery task)

├─ models/                     # Models
│  └─ crawl_job.py             # CrawlJob (Crawl job tree + SLA fields)
│  └─ page.py                  # Page (Metadata for each crawled page) models

├─ integrations/               # External system adapters
│  ├─ search_index_client.py   # OpenSearch adapter
│  ├─ blob_storage_client.py   # S3 adapter
│  ├─ http_client.py           # Fetch HTML via headless browser

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

### **3. Crawler Tasks (`tasks/`)**
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
- `tasks/crawl.py` – Main crawl pipeline (`run_crawl_job`)
- `models/page.py` – Page metadata
- `models/crawl_job.py` – CrawlJob

---

### **4. Integrations (`integrations/`)**
Unified adapters for external systems.

#### **Search Index Client (OpenSearch)**
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
- Tracks crawl status, timestamps (for SLA), metadata

#### **S3**
- Raw HTML (compressed)

#### **OpenSearch**
- Full-text search index
- Stores searchable content, title, snippet, metadata

#### **Redis**
- Celery broker + result backend
- Drives worker autoscaling based on queue depth metrics

---

This modular layout ensures clear separation of concerns between:
- **HTTP handlers**
- **Business logic**
- **Crawler pipeline**
- **External system adapters**
- **Data storage**

---
## Scaling, Clusters, load balancing config
- All heavy "Crawling" is running in Celery workers, which can be "autoscaled" horizontally by "Redis Broker queue length" metric
- Used AWS OpenSearch for search index (autoscaling is maintained by AWS)
- Used S3 for Blob storage, to prevent large SQL DB size
- Storing Pages/Jobs metadata SQLS DB (Postgres Cluster DB, which can use replicas/sharding)
- Added "cleanup" commands (Cron) to delete old "Jobs"


---
## ⚙️ Required services
- **Postgres** (defaults to SQLite when `DATABASE_URL` is unset)
- **Redis** (`REDIS_URL`) Celery broker/result backend
- **S3-compatible storage** for raw HTML (AWS S3)
- **OpenSearch** cluster (`OPENSEARCH_HOST`, credentials)


---
## 🚀 Run locally

From the project root (`manage.py` directory):

```bash
# 1. Create and activate a virtualenv
python -m venv venv
source venv/bin/activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install the Playwright browsers used for crawling
playwright install

# 4. Apply database migrations (SQLite/Postgres depending on DATABASE_URL)
python manage.py migrate

# 5. Start shared infrastructure (if not using managed services)
redis-server # or: docker run --rm -p 6379:6379 redis:7

# 6. Start a Celery worker (keep running in separate terminal)
celery -A app.celery worker -O fair -l INFO

# 7. (Optional) run the cleanup cron manually
python manage.py cleanup_jobs --days 7

# 8. Start the Django development server
python manage.py runserver 8000