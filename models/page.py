# crawler/models/pages.py
from django.db import models


class Page(models.Model):
    job = models.ForeignKey("models.CrawlJob", on_delete=models.CASCADE, related_name="pages")
    url = models.URLField(max_length=2048)

    last_crawled_at = models.DateTimeField(null=True, blank=True)
    http_status = models.IntegerField(null=True, blank=True)
    storage_key_raw = models.CharField(max_length=512, null=True, blank=True)
    search_index_key = models.CharField(max_length=512, null=True, blank=True)

    error = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ("job", "url")  # enforce visited-page tracking
