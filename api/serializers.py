from rest_framework import serializers


class CrawlSubmitSerializer(serializers.Serializer):
    """Serializer for crawl job submission."""
    url = serializers.URLField(required=True, help_text="URL to crawl")
    max_depth = serializers.IntegerField(
        required=False,
        default=2,
        min_value=1,
        help_text="Maximum crawl depth (default: 2)"
    )
    max_pages = serializers.IntegerField(
        required=False,
        default=100,
        min_value=1,
        help_text="Maximum number of pages to crawl (default: 100)"
    )


class CrawlStatusRequestSerializer(serializers.Serializer):
    """Serializer for crawl status lookup request."""
    job_id = serializers.UUIDField(required=True, help_text="Existing crawl job identifier")


class CrawlStatusSerializer(serializers.Serializer):
    """Serializer for crawl job status response."""
    job_id = serializers.UUIDField(read_only=True)
    status = serializers.CharField(read_only=True)
    url = serializers.URLField(read_only=True)
    pages_crawled = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class SearchRequestSerializer(serializers.Serializer):
    """Serializer for search request."""
    q = serializers.CharField(required=True, help_text="Search query")
    size = serializers.IntegerField(
        required=False,
        default=10,
        min_value=1,
        max_value=100,
        help_text="Number of results (default: 10, max: 100)"
    )
    from_ = serializers.IntegerField(
        required=False,
        default=0,
        min_value=0,
        source='from',
        help_text="Offset for pagination (default: 0)"
    )


class SearchHitSerializer(serializers.Serializer):
    """Serializer for individual search result."""
    url = serializers.URLField(read_only=True)
    title = serializers.CharField(read_only=True)
    score = serializers.FloatField(read_only=True)


class SearchResponseSerializer(serializers.Serializer):
    """Serializer for search response."""
    total = serializers.IntegerField(read_only=True)
    hits = SearchHitSerializer(many=True, read_only=True)


class PageDetailsRequestSerializer(serializers.Serializer):
    """Serializer for page details request."""
    page_id = serializers.IntegerField(required=True, help_text="Crawled page identifier")
