from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from models.crawl_job import CrawlJob


class Command(BaseCommand):
    help = 'Delete crawl jobs older than 30 days'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Delete jobs older than this many days (default: 30)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']

        # Calculate the cutoff date
        cutoff_date = timezone.now() - timedelta(days=days)

        # Find old jobs
        old_jobs = CrawlJob.objects.filter(requested_at__lt=cutoff_date)
        count = old_jobs.count()

        if count == 0:
            self.stdout.write(
                self.style.SUCCESS(f'No jobs older than {days} days found.')
            )
            return

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would delete {count} job(s) older than {days} days '
                    f'(before {cutoff_date.strftime("%Y-%m-%d %H:%M:%S")})'
                )
            )
            # Show a sample of jobs that would be deleted
            sample_jobs = old_jobs[:5]
            for job in sample_jobs:
                self.stdout.write(f'  - {job.id}: {job.url} (requested: {job.requested_at})')
            if count > 5:
                self.stdout.write(f'  ... and {count - 5} more')
        else:
            deleted_count, _ = old_jobs.delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted {deleted_count} job(s) older than {days} days.'
                )
            )