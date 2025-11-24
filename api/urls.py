"""
URL configuration for api app.

"""
from django.urls import path
from api.views import CrawlSubmitView, CrawlStatusView, SearchView, PageDetailsView


urlpatterns = [
    path('crawl/', CrawlSubmitView.as_view(), name='crawl'),
    path('crawl/<job_id>/', CrawlStatusView.as_view(), name='crawl-status'),
    path('search/', SearchView.as_view(), name='search'),
    path('page/<page_id>/', PageDetailsView.as_view(), name='page'),
]
