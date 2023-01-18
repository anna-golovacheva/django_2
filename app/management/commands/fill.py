from django.core.management import BaseCommand
from django.core import management


class Command(BaseCommand):
    def handle(self, *args, **options):
        management.call_command('flush', verbosity=0, interactive=False)
        management.call_command('loaddata', 'fixtures.json', verbosity=0)
