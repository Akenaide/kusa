import os
import json

from django.core.management.base import BaseCommand

from card.import_prices import import_prices


class Command(BaseCommand):
    help = "Import json"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str)

    def handle(self, *args, **options):
        with open(options["json_file"], 'r') as f:
            data = json.load(f)
            timestamp = os.path.splitext(f.name.split("-", 1)[1])[0]
        import_prices(data, timestamp)
