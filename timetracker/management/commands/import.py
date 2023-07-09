from django.core.management import BaseCommand

from timetracker.importer import TimeSliceImporter

class Command(BaseCommand):
    help = "import from DATA_DIR/import.tsv"

    def handle(self, *args, **options):
        TimeSliceImporter().import_tsv_file()

