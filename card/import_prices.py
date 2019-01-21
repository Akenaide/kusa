import arrow

from card import models


START = 1000


def import_prices(data, timestamp, chunk=START):
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
