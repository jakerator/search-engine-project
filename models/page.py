# crawler/models/pages.py
from django.db import models


class Page(models.Model):
    """
    Represents a single crawled page metadata and storage references.
    """
    job = models.ForeignKey("models.CrawlJob", on_delete=models.SET_NULL, null=True, blank=True, related_name="pages")
    url = models.URLField(max_length=2048)

    last_crawled_at = models.DateTimeField(null=True, blank=True)
    http_status = models.IntegerField(null=True, blank=True)
    storage_key_raw = models.CharField(max_length=512, null=True, blank=True)
    search_index_key = models.CharField(max_length=512, null=True, blank=True)

    error = models.TextField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        # Delete from blob storage if exists
        if self.storage_key_raw:
            try:
                from integrations.blob_storage_client import BlobStorageClient
                blob_client = BlobStorageClient()
                blob_client.delete(self.storage_key_raw)
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to delete blob for page {self.id}: {e}")

        # Delete from search index if exists
        if self.search_index_key:
            try:
                from integrations.search_index_client import SearchIndexClient
                search_client = SearchIndexClient()
                search_client.delete_page(self.search_index_key)
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to delete search index for page {self.id}: {e}")
        return super().delete(*args, **kwargs)

    class Meta:
        unique_together = ("job", "url")  # enforce visited-page tracking
