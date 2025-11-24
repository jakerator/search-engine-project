from django.contrib import admin
from .crawl_job import CrawlJob
from .page import Page


@admin.register(CrawlJob)
class CrawlJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'url', 'status', 'requested_at', 'started_at', 'finished_at']
    list_filter = ['status', 'requested_at']
    search_fields = ['url', 'id']
    readonly_fields = ['id', 'requested_at', 'started_at', 'finished_at']
    ordering = ['-requested_at']

    fieldsets = (
        ('Job Information', {
            'fields': ('id', 'url', 'status')
        }),
        ('Limits', {
            'fields': ('max_depth', 'max_pages')
        }),
        ('Timestamps', {
            'fields': ('requested_at', 'started_at', 'finished_at')
        }),
    )


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['id', 'job', 'url', 'storage_key_raw', 'http_status', 'last_crawled_at']
    list_filter = ['http_status', 'last_crawled_at']
    search_fields = ['url', 'job__id']
    readonly_fields = ['id', 'job', 'url']
    ordering = ['-last_crawled_at']

    fieldsets = (
        ('Page Information', {
            'fields': ('id', 'job', 'url')
        }),
        ('Crawl Details', {
            'fields': ('http_status', 'last_crawled_at', 'error')
        }),
    )