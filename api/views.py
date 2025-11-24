from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse
from api.serializers import (
    CrawlSubmitSerializer,
    CrawlStatusRequestSerializer,
    CrawlStatusSerializer,
    SearchRequestSerializer,
    SearchResponseSerializer,
    PageDetailsRequestSerializer,
)
from datetime import datetime
from services.crawl_service import CrawlService, SLAExceededError
from services.page_service import PageService
from services.search_service import SearchService


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    """Browsable API root listing core endpoints."""

    return Response({
        "crawl": reverse('crawl', request=request, format=format),
        "crawl-status": reverse('crawl-status', request=request, format=format, kwargs={'job_id': ':job_id'}),
        "search": reverse('search', request=request, format=format),
        "page": reverse('page', request=request, format=format, kwargs={'page_id': ':page_id'}),
    })


class CrawlSubmitView(GenericAPIView):
    """
    Handle crawl job submission.

    POST /api/crawl/
    """
    permission_classes = [AllowAny]
    serializer_class = CrawlSubmitSerializer  # request payload

    def post(self, request, *args, **kwargs):
        """
        Accepts JSON payload like: {"url": "https://example.com"}
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data["url"]
        max_depth = serializer.validated_data.get("max_depth", 2)
        max_pages = serializer.validated_data.get("max_pages", 100)

        try:
            # Call crawl_service to create job and queue crawl task
            job_data = CrawlService.submit_crawl(
                url=url,
                max_depth=max_depth,
                max_pages=max_pages
            )

            response_data = {
                "job_id": job_data["job_id"],
                "status": job_data["status"],
                "url": job_data["url"],
                "pages_crawled": 0,
                "created_at": job_data["requested_at"],
            }

            response_serializer = CrawlStatusSerializer(response_data)
            return Response(response_serializer.data, status=status.HTTP_202_ACCEPTED)

        except SLAExceededError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class CrawlStatusView(GenericAPIView):
    """
    Handle crawl job status lookup.

    GET /api/crawl/<job_id>/
    """
    permission_classes = [AllowAny]
    serializer_class = CrawlStatusRequestSerializer  # used for validating job_id

    def get(self, request, job_id, *args, **kwargs):
        """
        Expects job_id as path parameter: /api/crawl/<job_id>/
        """
        # Validate job_id using serializer (mainly type checking)
        data = {"job_id": job_id}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        job_id = serializer.validated_data["job_id"]

        try:
            # Query actual job status from database/service
            response_data = CrawlService.get_job_status(job_id)
            response_serializer = CrawlStatusSerializer(response_data)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Job not found: {job_id}"},
                status=status.HTTP_404_NOT_FOUND
            )


class SearchView(GenericAPIView):
    """
    Handle search queries across indexed pages.

    GET /api/search/?q=<query>&size=<size>&from=<from>
    """
    permission_classes = [AllowAny]
    serializer_class = SearchRequestSerializer

    def get(self, request, *args, **kwargs):
        """
        Search for pages matching the query.
        Query params: q (required), size (optional, default 10), from (optional, default 0)
        """
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        query = serializer.validated_data["q"]
        size = serializer.validated_data.get("size", 10)
        from_ = serializer.validated_data.get("from", 0)

        try:
            results = SearchService.search(query=query, size=size, from_=from_)
            response_serializer = SearchResponseSerializer(results)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Search failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PageDetailsView(GenericAPIView):
    """
    Handle retrieval of individual page details by page ID.

    GET /api/page/<page_id>/
    """
    permission_classes = [AllowAny]
    serializer_class = PageDetailsRequestSerializer
    # used for validating job_id

    def get(self, request, page_id, *args, **kwargs):
        """
        Expects page_id as path parameter: /api/page/<page_id>/
        """
        # Validate page_id using serializer (mainly type checking)
        data = {"page_id": page_id}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        page_id = serializer.validated_data["page_id"]

        try:
            # Call search service or database to get page details
            page_details = PageService.get_page_details(page_id)

            if not page_details:
                return Response(
                    {"error": f"Page not found: {page_id}"},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(page_details, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve page details: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )