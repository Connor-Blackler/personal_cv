from django.core.management.base import BaseCommand
from core.tasks import scrape_and_save


class Command(BaseCommand):
    help = 'Perform scraping and save the data'

    def handle(self, *args, **options):
        self.stdout.write('Performing scraping and saving...')
        scrape_and_save()
        self.stdout.write(self.style.SUCCESS(
            'Scraping and saving completed successfully.'))
