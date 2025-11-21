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

