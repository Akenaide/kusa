import asyncio
import os
import json

import arrow
from django.core.management.base import BaseCommand
from card import models

START = 1000

class Command(BaseCommand):
    help = "Import json"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str)

    def handle(self, *args, **options):
        chunk = START
        prices = []
        futures = []
        with open(options["json_file"], 'r') as f:
            data = json.load(f)
            timestamp = os.path.splitext(f.name.split("-", 1)[1])[0]

        timestamp = arrow.get(timestamp).datetime
        async def createcard(future, card_id, value):
            # print(card_id)
            card, _ = models.Card.objects.get_or_create(card_id=card_id,
                    image=value["URL"],
                    yyt=value["CardURL"],
                    rarity=value["Rarity"],
                    )
            prices.append(models.Price(card=card,
                    value=value["Price"],
                    timestamp=timestamp,
                    ))
            future.set_result("")

        for card_id, value in data.items():
            future = asyncio.Future()
            futures.append(future)
            asyncio.ensure_future(createcard(future, card_id, value))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*futures))
        loop.close()
        for _ in range(len(prices) // START + 1):
            # print(chunk)
            models.Price.objects.bulk_create(prices[chunk - START:chunk])
            chunk += START
