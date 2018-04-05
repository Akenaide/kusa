import os
import json

import arrow
from django.core.management.base import BaseCommand, CommandError
from card import models

class Command(BaseCommand):
    help = "Import json"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str)

    def handle(self, *args, **options):
        with open(options["json_file"], 'r') as f:
            data = json.load(f)
            timestamp = os.path.splitext(f.name.split("-", 1)[1])[0]
            timestamp = arrow.get(timestamp).datetime
            for card_id, value in data.items():
                card, _ = models.Card.objects.get_or_create(card_id=card_id,
                        image=value["URL"],
                        yyt=value["CardURL"],
                        rarity=value["Rarity"],
                        )
                card.save()
                models.Price.objects.create(card=card,
                        value=value["Price"],
                        timestamp=timestamp,
                        )
