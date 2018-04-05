import datetime

from django.shortcuts import render
import arrow

from card import models

# Create your views here.

def home(request):
    d1 = arrow.get("2018-04-01")
    d2 = arrow.get("2018-04-05")
    cols = []

    for card in models.Card.objects.all()[:500]:
        try:
            price1 = card.price_set.get(timestamp=d1.datetime)
            price2 = card.price_set.get(timestamp=d2.datetime)
            if price1.value == price2.value:
                continue
        except models.Price.DoesNotExist:
            pass
        else:
            cols.append((price1, price2,))

    context = {
            "cols": cols,
            "dates": [d1, d2,],
            }
    return render(request, "home.html", context=context)
