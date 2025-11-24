# crawler/tasks.py
from collections import deque
from datetime import timedelta
import os
from celery import shared_task
from django.utils import timezone

from models.crawl_job import CrawlJob
from models.page import Page
from integrations.http_client import HeadlessBrowser
from integrations.blob_storage_client import BlobStorageClient
from integrations.search_index_client import SearchIndexClient


@shared_task(bind=True)
def run_crawl_job(self, job_id, url, sla_duration_hours: int):
    """
    Single task that crawls within single session (to prevent IP rotation, RAM/CPU spikes, anti-bot checks etc).:
      - root page
      - all children pages
    Optimized for predictable RAM/CPU usage, designed for multiple workers scalability.

    Uses the Page table for visited tracking.

    If need even more scalability, it can be split into multiple tasks (per page), but
    that adds complexity around state management, task chaining, and makes IP rotation possible
    (which isn't described in project requirements).

    """

    PAGE_EXPIRE_HRS = int(os.environ.get("PAGE_EXPIRE_HRS", 24))  # How long to keep page data before re-crawling

    job = CrawlJob.objects.get(pk=job_id)
    job.mark_running()

    # Calculate SLA deadline
    sla_deadline = job.requested_at + timedelta(hours=sla_duration_hours)

    # Track pages discovered in this crawl session
    pages_discovered = 0

    frontier = deque([(job.url, 0)])  # (url, depth)
    blob_storage_client = BlobStorageClient()
    search_index_client = SearchIndexClient()

    try:
        # Reuse a single headless browser across all page fetches for efficiency.
        with HeadlessBrowser() as browser:
            while frontier:

                # Check SLA - break if we've exceeded the time limit (return what's been done so far)
                if timezone.now() >= sla_deadline:
                    break

                # limit by pages
                if pages_discovered >= job.max_pages:
                    break
                pages_discovered += 1

                url, depth = frontier.popleft()

                # Skip if page exists and was crawled within PAGE_EXPIRE_HRS; otherwise allow re-crawl
                expire_cutoff = timezone.now() - timedelta(hours=PAGE_EXPIRE_HRS)
                check_page = Page.objects.filter(url=url).first()
                if check_page:
                    if check_page.last_crawled_at and check_page.last_crawled_at >= expire_cutoff:
                        continue  # Fresh enough; skip
                    else:
                        check_page.delete()  # Stale; remove to allow fresh crawl

                # Create a Page entry
                page = Page.objects.create(job=job, url=url)


                try:
                    # Fetch the page via reusable browser
                    html, plain_text, title, child_links, status_code = browser.fetch_html(url)

                    # Save raw html in BLOB storage
                    raw_key = blob_storage_client.store(page_id=page.id, content=html)

                    # Send to Index storage
                    doc_id = search_index_client.index_page(
                        url=url,
                        title=title,
                        content=plain_text,
                        page_id=page.id,
                        last_crawled_at=timezone.now(),
                    )

                    # Update page
                    page.last_crawled_at = timezone.now()
                    page.http_status = status_code
                    page.storage_key_raw = raw_key
                    page.search_index_key = doc_id
                    page.save(update_fields=[
                        "last_crawled_at",
                        "http_status",
                        "storage_key_raw",
                        "search_index_key",
                    ])


                    # Queue links (children)
                    if depth < job.max_depth:
                        # child_links = [] # DEBUG

                        for link in child_links:
                            frontier.append((link, depth + 1))

                except Exception as e:
                    # Mark page failed
                    page.error = str(e)
                    page.save(update_fields=["error"])

                    continue

        # Completed
        search_index_client.refresh_index()
        job.mark_completed()

    except Exception:
        job.mark_failed()
        raise
