"""
BlobStorageClient - S3 integration for storing crawled page content
"""

import hashlib
import logging
from datetime import datetime
from typing import Optional
import boto3
from botocore.exceptions import ClientError
from django.conf import settings


logger = logging.getLogger(__name__)


class BlobStorageClient:
    """Client for storing crawled page content in AWS S3."""

    def __init__(self):
        """Initialize S3 client with AWS credentials from Django settings."""
        self.bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'search-engine-crawl-data')

        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID', None),
            aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
            region_name=getattr(settings, 'AWS_REGION', 'us-east-1'),
        )

    def store(self, page_id: int, content: str) -> str:
        """Persist the HTML body for a page and return the generated key.

        Args:
            page_id: Database primary key of the `Page` record. Used to
                partition objects underneath `crawls/{page_id}/` for easier
                cleanup/retention policies.
            content: Raw HTML (or serialized text) that should be written to S3.

        Returns:
            str: The storage key (from :meth:`_generate_key`) that callers can
            cache on the `Page` row for future retrieval.
        """
        storage_key = self._generate_key(page_id)

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=storage_key,
            Body=content.encode('utf-8'),
            ContentType='text/html',
        )

        logger.info(f"Stored content at {storage_key}")
        return storage_key

    def retrieve(self, storage_key: str) -> Optional[str]:
        """
        Retrieve page content from S3.

        Args:
            storage_key: The S3 key

        Returns:
            str: The stored content, or None if not found
        """
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=storage_key
            )
            return response['Body'].read().decode('utf-8')
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                return None
            raise

    def delete(self, storage_key: str) -> None:
        """Delete content from S3."""
        self.s3_client.delete_object(
            Bucket=self.bucket_name,
            Key=storage_key
        )

    def _generate_key(self, page_id: str) -> str:
        """Generate S3 storage key: crawls/{page_id}/{timestamp}.html"""
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
        return f"crawls/{page_id}/{timestamp}.html"