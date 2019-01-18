import asyncio
import os
import json

import arrow
from django.core.management.base import BaseCommand
from card import models

START = 1000


def import_price(data, timestamp, chunk=START):
    prices = []
    timestamp = arrow.get(timestamp).datetime

    for card in models.Card.objects.all():
        try:
            new_data = data[card.card_id]
        except KeyError:
            continue
        new_data["to_delete"] = True
        prices.append(models.Price(card=card,
                                   value=new_data["Price"],
                                   timestamp=timestamp,
                                   ))

    new_cards = {key: data for key,
                 data in data.items() if "to_delete" not in data}

    for card_id, value in new_cards.items():
        card = models.Card.objects.create(card_id=card_id,
                                          image=value["URL"],
                                          yyt=value["CardURL"],
                                          rarity=value["Rarity"],
                                          )

        prices.append(models.Price(card=card,
                                   value=value["Price"],
                                   timestamp=timestamp,
                                   ))

    for _ in range(len(prices) // START + 1):
        models.Price.objects.bulk_create(prices[chunk - START:chunk])
        chunk += START


class Command(BaseCommand):
    help = "Import json"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str)

    def handle(self, *args, **options):
        with open(options["json_file"], 'r') as f:
            data = json.load(f)
            timestamp = os.path.splitext(f.name.split("-", 1)[1])[0]
        import_price(data, timestamp)
