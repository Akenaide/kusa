import datetime

from django.shortcuts import render
import arrow

from card import models

# Create your views here.

def home(request):
    d1 = arrow.get("2018-04-01")
    d2 = arrow.get("2018-04-05")
    p = defaultdict(list)


    for prices in models.Price.objects.filter(timestamp__in=[d1.datetime, d2.datetime]).select_related("card").order_by("timestamp"):
        p[prices.card.card_id].append(prices)

    cols =  [v for k, v in p.items() if len(v) > 1]
    context = {
            "cols": cols,
            "dates": [d1, d2,],
            }
    r = render(request, "home.html", context=context)
    return r
