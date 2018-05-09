from collections import defaultdict

from django.shortcuts import render
import arrow

from card import models

def home(request):
    if "dates" in request.GET:
        dates = request.GET.get("dates").split(",")
    else:
        dates = list(models.Price.objects.values_list("timestamp", flat=True).distinct())[-2:]

    d1 = arrow.get(dates[0])
    d2 = arrow.get(dates[1])
    p = defaultdict(list)
    cols = []


    for price in models.Price.objects.filter(timestamp__in=[d1.datetime.isoformat(),
            d2.datetime.isoformat()]).select_related("card").order_by("timestamp"):
        p[price.card.card_id].append(price)

    for _, value in p.items():
        if len(value) != 2:
            continue
        if value[0].value != value[1].value:
            cols.append(value)

    context = {
            "cols": cols,
            "dates": [d1, d2,],
            }
    r = render(request, "home.html", context=context)
    return r

def detail(request, card_id):
    card = models.Card.objects.get(card_id=card_id)
    context = {
            "card": card,
            "prices": card.price_set.all().order_by("timestamp"),
            }
    r = render(request, "detail.html", context=context)
    return r
