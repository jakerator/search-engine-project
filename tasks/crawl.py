# crawler/tasks.py
from collections import deque
from datetime import timedelta
import os
from celery import shared_task
from django.db import models as dj_models
from django.utils import timezone

from models.crawl_job import CrawlJob
from crawler.models.pages import Page
from integrations.http_client import HeadlessBrowser
from integrations.s3_client import store_raw_html, store_parsed_content
from integrations.opensearch_client import index_page_document
from crawler.link_filter import normalize_and_filter_links


@shared_task(bind=True, max_retries=3, soft_time_limit=300)
def run_crawl_job(self, job_id: str, sla_duration_hours: int):
    """
    Single task that crawls withing single session (to prevent IP rotation):
      - root page
      - all children pages
    Uses the Page table for visited tracking.

    If need even more scalability, it can be split into multiple tasks per page, but
    that adds complexity around state management, task chaining, and makes IP rotation posible
    (which isn't described in project requirements).

    """

    PAGE_EXPIRE_HRS = int(os.environ.get("PAGE_EXPIRE_HRS", 24))  # How long to keep page data before re-crawling

    job = CrawlJob.objects.get(pk=job_id)
    job.mark_running()

    # Calculate SLA deadline
    sla_deadline = job.requested_at + timedelta(hours=sla_duration_hours)

    frontier = deque([(job.url, 0)])  # (url, depth)

    with HeadlessBrowser() as browser:
        try:
            while frontier:

                # Check SLA - break if we've exceeded the time limit (return what's been done so far)
                if timezone.now() >= sla_deadline:
                    break

                # limit by pages
                if job.pages_discovered >= job.max_pages:
                    break

                url, depth = frontier.popleft()

                # Skip if page exists and was crawled within PAGE_EXPIRE_HRS; otherwise allow re-crawl
                expire_cutoff = timezone.now() - timedelta(hours=PAGE_EXPIRE_HRS)
                check_page = Page.objects.get(url=url)
                if check_page:
                    if check_page.last_crawled_at and check_page.last_crawled_at >= expire_cutoff:
                        continue  # Fresh enough; skip
                    else:
                        check_page.delete()  # Stale; remove to allow fresh crawl

                # Create a Page entry
                page = Page.objects.create(job=job, url=url, depth=depth)

                try:
                    # Fetch the page
                    html, plain_text, title, status_code = browser.fetch_html(url)

                    # Save raw html in BLOB storage
                    raw_key = store_raw_html(job_id=str(job.id), url=url, html=html)

                    # Index in OpenSearch
                    index_page_document(
                        url=url,
                        title=title,
                        plain_text=plain_text,
                        job_id=str(job.id),
                        depth=depth,
                        last_crawled_at=timezone.now(),
                    )

                    # Update page
                    page.last_crawled_at = timezone.now()
                    page.http_status = status_code
                    page.storage_key_raw = raw_key
                    page.save(update_fields=[
                        "last_crawled_at",
                        "http_status",
                        "storage_key_raw",
                    ])


                    # Extract links (children)
                    if depth < job.max_depth:
                        child_links = normalize_and_filter_links(url, html)
                        for link in child_links:
                            frontier.append((link, depth + 1))

                except Exception as e:
                    # Mark page failed
                    page.error = str(e)
                    page.save(update_fields=["error"])

                    continue

            # Completed
            job.mark_completed()

        except Exception:
            job.mark_failed()
            raise
