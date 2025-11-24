""" Get page details from SQL DB, attach BLOB data """


from models.page import Page
from integrations.blob_storage_client import BlobStorageClient


class PageService():
    @classmethod
    def get_page_details(cls, page_id: str) -> dict | None:
        """
        Retrieve page details by page ID.

        Args:
            page_id (str): The ID of the page to retrieve

        Returns:
            dict | None: Page details if found, else None
        """
        try:
            page = Page.objects.get(id=page_id)
        except Page.DoesNotExist:
            return None

        # Retrieve blob content if storage key exists
        blob_content = None
        if page.storage_key_raw:
            blob_storage_client = BlobStorageClient()
            blob_content = blob_storage_client.retrieve(page.storage_key_raw)

        # Construct the response dictionary
        page_details = {
            "id": str(page.id),
            "url": page.url,
            "title": getattr(page, 'title', None),
            "content": blob_content,
            "metadata": getattr(page, 'metadata', None),
            "crawled_at": page.last_crawled_at.isoformat() if page.last_crawled_at else None,
            "http_status": page.http_status,
            "storage_key": page.storage_key_raw,
            "search_index_key": page.search_index_key,
            "error": page.error,
        }

        return page_details
