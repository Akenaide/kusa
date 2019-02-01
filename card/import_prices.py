import logging

import arrow
from django.core.exceptions import ValidationError

from card import models


START = 1000
logger = logging.getLogger(__name__)


def parse_prices(data, timestamp):
    """
    prepare data before import
    """

    prices = []

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
    return prices


def import_prices(data, timestamp, chunk=START):

    timestamp = arrow.get(timestamp).datetime
    prices = parse_prices(data, timestamp)

    for price in prices:
        price.card.save()
        try:
            price.save()
        except ValidationError as e:
            logger.warning(e)
