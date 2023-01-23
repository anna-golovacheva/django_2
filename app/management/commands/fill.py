from django.core.management import BaseCommand
from django.core import management


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("args", metavar="fixture", nargs="+", help="Fixture labels.")

    def handle(self, *args, **options):
        management.call_command('flush', verbosity=0, interactive=False)
        print('loading data from fixtures')
        management.call_command('loaddata', args[0], verbosity=0)
