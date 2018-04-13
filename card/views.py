from collections import defaultdict

from django.shortcuts import render
import arrow

from card import models

# Create your views here.

def home(request):
    dates = request.GET.get("dates").split(",")
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
