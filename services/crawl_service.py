"""
CrawlService - Business logic for crawl job management

Responsibilities:
- Create crawl jobs (root URLs only)
- Enforce 1-hour SLA logic
- Push crawl tasks to Redis/Celery
- Aggregate job status from Postgres
"""

import uuid
from datetime import timedelta
from django.utils import timezone
from models.crawl_job import CrawlJob


class SLAExceededError(Exception):
    pass


class CrawlService:
    """
    Service for managing web crawl jobs with SLA enforcement.
    Creates CrawlJob records only for root URLs.
    """

    # SLA Configuration
    SLA_DURATION_HOURS = 1  # 1-hour SLA for crawl completion
    DEFAULT_MAX_DEPTH = 3
    DEFAULT_MAX_PAGES = 100

    @classmethod
    def submit_crawl(cls, url, max_depth=None, max_pages=None):
        """
        Submit a crawl job for a root URL.

        Args:
            url (str): The URL to crawl
            max_depth (int, optional): Maximum recursion depth
            max_pages (int, optional): Maximum pages to crawl

        Returns:
            dict: Job details including job_id, status, and SLA deadline

        Raises:
            SLAExceededError: If SLA is currently exceeded
        """
        # Check SLA before creating new job
        if not cls._is_within_sla():
            raise SLAExceededError("SLA exceeded; new crawl jobs are not accepted at this time, try later")

        # Apply defaults
        if max_depth is None:
            max_depth = cls.DEFAULT_MAX_DEPTH
        if max_pages is None:
            max_pages = cls.DEFAULT_MAX_PAGES

        # Create root job
        job_id = uuid.uuid4()
        job = CrawlJob.objects.create(
            id=job_id,
            url=url,
            status="queued",
            max_depth=max_depth,
            max_pages=max_pages,
            requested_at=timezone.now(),
        )

        # Queue the crawl task
        cls._queue_crawl_task(job.id, url, max_depth=job.max_depth, max_pages=job.max_pages)

        return {
            "job_id": str(job.id),
            "url": job.url,
            "status": job.status,
            "requested_at": job.requested_at.isoformat(),
            "max_depth": job.max_depth,
            "max_pages": job.max_pages,
        }

    @classmethod
    def get_job_status(cls, job_id):
        """
        Get status of a crawl job.

        Args:
            job_id (UUID ): The job ID to query

        Returns:
            dict: Job status with simple format matching CrawlStatusSerializer

        Raises:
            CrawlJob.DoesNotExist: If job not found
        """
        job = CrawlJob.objects.get(id=job_id)

        # Since we only create jobs for root URLs, pages_crawled would be 1 if completed, 0 otherwise
        pages_crawled = 1 if job.status == "completed" else 0

        return {
            "job_id": job.id,
            "status": job.status,
            "url": job.url,
            "pages_crawled": pages_crawled,
            "created_at": job.requested_at,
        }


    @classmethod
    def _is_within_sla(cls):
        """
        Check if there are any jobs in the system that exceeded SLA.

        Returns:
            bool: True if no jobs exceeded SLA, False otherwise
        """
        # Check if any jobs in the entire database are beyond SLA
        cutoff_time = timezone.now() - timedelta(hours=cls.SLA_DURATION_HOURS)
        jobs_beyond_sla = CrawlJob.objects.filter(
            status__in=["queued", "running"],
            requested_at__lt=cutoff_time
        ).exists()

        return not jobs_beyond_sla

    @classmethod
    def _queue_crawl_task(cls, job_id, url, max_depth, max_pages):
        """
        Queue a crawl task to Celery.

        Args:
            job_id (UUID): Job ID
            url (str): URL to crawl
            max_depth (int): Maximum recursion depth
            max_pages (int): Maximum pages to crawl
        """
        # Import here to avoid circular dependency
        try:
            from crawler.tasks import crawl_page

            # Queue task to Celery
            crawl_page.delay(
                job_id=str(job_id),
                url=url,
                max_depth=max_depth,
                max_pages=max_pages,
                sla_duration_hours=cls.SLA_DURATION_HOURS,
            )
        except ImportError:
            # If Celery/tasks not yet implemented, log warning
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                f"crawler.tasks.crawl_page not available. Job {job_id} queued but not dispatched."
            )

