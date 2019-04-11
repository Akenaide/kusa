from django.db import models


class Card(models.Model):
    card_id = models.TextField(db_index=True, unique=True)
    image = models.SlugField(max_length=220)
    yyt = models.SlugField(max_length=220)
    rarity = models.TextField()

    def __str__(self):
        return self.card_id


class Price(models.Model):
    class Meta:
        unique_together = (('card', 'timestamp',),)

    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    value = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

    def __str__(self):
        return self.card_id


def compare_prices_from_date(date1: str, date2: str, search="") -> list:
    """
    Compare prices from given dates
    """

    cols = []

    first = Price.objects.select_related("card").filter(
        timestamp=date1).order_by("card__card_id")
    second = Price.objects.filter(timestamp=date2).only(
        "card_id",
        "value",
    )
    if search:
        first = first.filter(card__card_id__icontains=search.upper())
        second = second.filter(card__card_id__icontains=search.upper())

    second = {price.card_id: price.value for price in second}

    first_data = first.values(
        "card_id",
        "value",
        "card__image",
        "card__yyt",
        "card__card_id",
    )
    for price in first_data:
        try:
            second_price = second[price["card_id"]]
        except KeyError:
            # DB may have errors e.g cards change name
            continue
        else:
            if price["value"] != second_price:
                cols.append([price, second_price])

    return cols
