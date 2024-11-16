import csv
from django.core.management import BaseCommand
from accounts.models import Country

class Command(BaseCommand):
    help = 'Load Country csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt') as f:
            reader = csv.reader(f, dialect='excel')
            for row in reader:
                Country.objects.create(
                    id=row[0],
                    name=row[1],
                )