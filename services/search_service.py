"""
SearchService - Business logic for search operations

Responsibilities:
- Handle search queries
- Interface with SearchIndexClient
- Format search results
"""

import logging
from typing import Dict, Any, List, Optional
from integrations.search_index_client import SearchIndexClient


class SearchService:
    """
    Service for managing search operations across indexed pages.
    """

    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100

    @classmethod
    def search(cls, query: str, size: Optional[int] = None, from_: int = 0) -> Dict[str, Any]:
        """
        Search indexed pages.

        Args:
            query (str): The search query string
            size (int, optional): Number of results to return (default: 10, max: 100)
            from_ (int): Offset for pagination (default: 0)

        Returns:
            dict: Search results with total count and hits

        Raises:
            ValueError: If parameters are invalid
        """
        # Validate and apply defaults
        if size is None:
            size = cls.DEFAULT_PAGE_SIZE

        if size < 1 or size > cls.MAX_PAGE_SIZE:
            raise ValueError(f"Size must be between 1 and {cls.MAX_PAGE_SIZE}")

        if from_ < 0:
            raise ValueError("Offset (from) must be non-negative")

        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        # Perform search
        try:
            search_client = SearchIndexClient()
            results = search_client.search(query=query.strip(), size=size, from_=from_)
        
            return results

        except Exception as e:
            raise