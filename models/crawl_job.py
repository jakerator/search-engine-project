import uuid
from django.db import models
from django.utils import timezone


class CrawlJob(models.Model):
    """
    Represents a single crawl request. A full crawl may consist of:
      - One root job (requested via API)
      - Multiple child jobs discovered during crawling (links)

    """

    JOB_STATUS_CHOICES = [
        ("queued", "Queued"),
        ("running", "Running"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # What page this job is crawling
    url = models.URLField(max_length=2048)

    # Job lifecycle fields
    status = models.CharField(
        max_length=20, choices=JOB_STATUS_CHOICES, default="queued"
    )

    # date/time fields will be used for SLA calculations , auto-scaling etc
    requested_at = models.DateTimeField(default=timezone.now)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    # Limits (only meaningful for root jobs)
    max_depth = models.IntegerField(null=True, blank=True)
    max_pages = models.IntegerField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["requested_at"]),
        ]

    # ----------------------------------------------------------------------
    # Convenience API
    # ----------------------------------------------------------------------

    def mark_running(self):
        self.status = "running"
        self.started_at = timezone.now()
        self.save(update_fields=["status", "started_at"])

    def mark_completed(self):
        self.status = "completed"
        self.finished_at = timezone.now()
        self.save(update_fields=["status", "finished_at"])

    def mark_failed(self, error_message):
        self.status = "failed"
        self.finished_at = timezone.now()
        self.save(update_fields=["status", "finished_at"])

    def __str__(self):
        return f"CrawlJob({self.id}, url={self.url}, status={self.status})"
