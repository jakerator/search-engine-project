from django.contrib import admin
from .crawl_job import CrawlJob


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
