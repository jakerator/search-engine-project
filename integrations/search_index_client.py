"""
SearchIndexClient - AWS OpenSearch integration for indexing crawled pages
"""

import logging
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3
from django.conf import settings

logger = logging.getLogger(__name__)


class SearchIndexClient:
    """Client for indexing crawled page content in AWS OpenSearch."""

    _instance = None
    _client = None

    def __new__(cls):
        """Singleton pattern to reuse client instances."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize OpenSearch client and ensure index exists."""
        if self._client is None:
            self.index_name = settings.OPENSEARCH_INDEX_NAME
            self._client = self._get_opensearch_client()
            self._ensure_index_exists()

    @property
    def client(self):
        """Thread-safe client access."""
        return self._client

    def _get_opensearch_client(self) -> OpenSearch:
        """Create and return an OpenSearch client instance with optimized settings."""
        host = getattr(settings, 'OPENSEARCH_HOST', 'localhost')
        port = getattr(settings, 'OPENSEARCH_PORT', 9200)
        region = getattr(settings, 'AWS_REGION', 'us-east-1')

        aws_access_key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
        aws_secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)

        common_config = {
            'hosts': [{'host': host, 'port': port}],
            'connection_class': RequestsHttpConnection,
            'timeout': 60,
            'max_retries': 3,
            'retry_on_timeout': True,
            'retry_on_status': (502, 503, 504),
            'maxsize': 25,  # Connection pool size
        }

        if aws_access_key and aws_secret_key:
            credentials = boto3.Session(
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=region,
            ).get_credentials()

            auth = AWSV4SignerAuth(credentials, region, 'es')

            return OpenSearch(
                http_auth=auth,
                use_ssl=True,
                verify_certs=True,
                **common_config
            )

        # Local/dev fallback
        return OpenSearch(
            use_ssl=False,
            verify_certs=False,
            **common_config
        )

    def _get_index_mapping(self) -> Dict[str, Any]:
        """Define the index mapping for crawled pages."""
        # Determine shards based on expected scale
        num_shards = getattr(settings, 'OPENSEARCH_NUM_SHARDS', 3)
        num_replicas = getattr(settings, 'OPENSEARCH_NUM_REPLICAS', 1)

        return {
            "settings": {
                "number_of_shards": num_shards,
                "number_of_replicas": num_replicas,
                "refresh_interval": "30s",  # Don't refresh too frequently
                "index.max_result_window": 10000,
                "analysis": {
                    "analyzer": {
                        "default": {
                            "type": "standard"
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "url": {
                        "type": "keyword"
                    },
                    "title": {
                        "type": "text",
                        "analyzer": "standard",
                        "fields": {
                            "keyword": {"type": "keyword"}
                        }
                    },
                    "content": {
                        "type": "text",
                        "analyzer": "standard"
                    },
                    "page_id": {
                        "type": "keyword"
                    },
                    "last_crawled_at": {
                        "type": "date",
                        "format": "strict_date_optional_time||epoch_millis"
                    },
                    "indexed_at": {
                        "type": "date",
                        "format": "strict_date_optional_time||epoch_millis"
                    }
                }
            }
        }

    def _ensure_index_exists(self) -> None:
        """Create index if it doesn't exist."""
        try:
            if not self.client.indices.exists(index=self.index_name):
                logger.info(f"Index '{self.index_name}' does not exist. Creating...")
                self.client.indices.create(
                    index=self.index_name,
                    body=self._get_index_mapping()
                )
                logger.info(f"Index '{self.index_name}' created successfully.")
            else:
                logger.debug(f"Index '{self.index_name}' already exists.")
        except Exception as e:
            logger.error(f"Failed to ensure index exists: {e}")
            raise

    def _generate_doc_id(self, url: str) -> str:
        """Generate a consistent document ID from URL."""
        return hashlib.sha256(url.encode('utf-8')).hexdigest()

    def index_page(
        self,
        url: str,
        title: str,
        content: str,
        page_id: str,
        last_crawled_at: Optional[datetime] = None,
        refresh: bool = False
    ) -> str:
        """Index a crawled page in OpenSearch."""
        document = {
            "url": url,
            "title": title,
            "content": content,
            "page_id": page_id,
            "last_crawled_at": (last_crawled_at or datetime.utcnow()).isoformat(),
            "indexed_at": datetime.utcnow().isoformat(),
        }

        doc_id = self._generate_doc_id(url)

        self.client.index(
            index=self.index_name,
            id=doc_id,
            body=document,
            refresh=refresh  # Optionally refresh index immediately
        )

        return doc_id

    def delete_page(self, doc_id: str) -> None:
        """Delete a single document from the search index."""
        try:
            self.client.delete(
                index=self.index_name,
                id=doc_id
            )
            logger.info(f"Document '{doc_id}' deleted from index '{self.index_name}'.")
        except Exception as e:
            logger.error(f"Failed to delete document '{doc_id}': {e}")
            # Don't raise - we want page deletion to succeed even if index deletion fails

    def search(self, query: str, size: int = 10, from_: int = 0) -> Dict[str, Any]:
        """Search indexed pages."""
        search_body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^2", "content"],
                }
            },
            "size": size,
            "from": from_,
        }

        response = self.client.search(index=self.index_name, body=search_body)

        return {
            "total": response["hits"]["total"]["value"],
            "hits": [
                {
                    "url": hit["_source"]["url"],
                    "title": hit["_source"]["title"],
                    "score": hit["_score"],
                }
                for hit in response["hits"]["hits"]
            ]
        }

    def delete_index(self) -> None:
        """Delete the index (useful for testing/cleanup)."""
        try:
            if self.client.indices.exists(index=self.index_name):
                self.client.indices.delete(index=self.index_name)
                logger.info(f"Index '{self.index_name}' deleted successfully.")
        except Exception as e:
            logger.error(f"Failed to delete index: {e}")
            raise

    def refresh_index(self) -> None:
        """Manually refresh the index to make recent changes searchable."""
        self.client.indices.refresh(index=self.index_name)
