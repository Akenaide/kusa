import http
import json

from django.shortcuts import render
from django.shortcuts import redirect
import arrow

from card import models
from card.import_prices import import_prices


def home(request):
    if "dates" in request.GET:
        dates = request.GET.get("dates").split(",")
    else:
        dates = list(models.Price.objects.values_list(
            "timestamp", flat=True).order_by("timestamp").distinct())[-2:]

    try:
        d1 = arrow.get(dates[0])
        d2 = arrow.get(dates[1])
    except IndexError:
        return render(request, "home.html", context={})

    context = {
        "cols": models.compare_prices_from_date(d1.isoformat(), d2.isoformat()),
        "dates": [d1, d2, ],
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


def import_json(request):
    """
    import json
    """

    client = http.client.HTTPSConnection("proxymaker.naide.moe")
    client.request("GET", "/static/yyt_infos-%s.json" % request.POST["date"])
    response = client.getresponse()
    data = json.loads(response.read().decode('utf-8'))
    import_prices(data, request.POST["date"])
    return redirect("home")
