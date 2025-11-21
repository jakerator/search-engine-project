"""
URL configuration for api app.

"""
from django.urls import path
from api.views import CrawlSubmitView, CrawlStatusView


urlpatterns = [
    path('crawl/', CrawlSubmitView.as_view(), name='crawl'),
    path('crawl/<job_id>/', CrawlStatusView.as_view(), name='crawl-status'),
]
