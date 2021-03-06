import http
import json

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
import arrow

from card import models
from card.import_prices import import_prices


def home(request):
    search = request.GET.get("search")
    msort = request.GET.get("sort")
    if "dates" in request.GET:
        dates = request.GET.getlist("dates")
    else:
        dates = list(models.TimeSP.objects.values_list(
            "value", flat=True).order_by("value"))[-2:]

    try:
        d1 = arrow.get(dates[0])
        d2 = arrow.get(dates[1])
    except IndexError:
        return render(request, "home.html", context={})

    cols = models.compare_prices_from_date(d1.isoformat(), d2.isoformat(), search=search)

    if msort == "diff":
        cols.sort(key=lambda x: x[2])

    context = {
        "cols": cols,
        "dates": [d1, d2, ],
        "available_date": models.TimeSP.objects.all().values_list("value", flat=True),
    }
    r = render(request, "home.html", context=context)
    return r


def detail(request, card_id):
    card = models.Card.objects.get(card_id__iexact=card_id)
    prices = []
    _prices = list(card.price_set.all().order_by("timestamp__value"))
    prices.append(_prices[0])

    for p, _ in enumerate(_prices):
        if not prices[-1].value == _prices[p].value:
            prices.append(_prices[p])

    description = [(v.timestamp.value.date().isoformat(), v.value)
                   for v in prices[-3:]]

    context = {
        "card": card,
        "prices": prices,
        "description": description,
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


def update_images(request):
    """
    update images
    """

    client = http.client.HTTPSConnection("proxymaker.naide.moe")
    client.request("GET", "/static/yyt_infos.json")
    response = client.getresponse()
    data = json.loads(response.read().decode('utf-8'))

    for card in models.Card.objects.filter(
            image__contains="noimage").only("card_id", "image"):
        try:
            card_data = data[card.card_id]
        except KeyError:
            continue
        card.image = card_data["URL"]
        card.save()

    return redirect("home")


def api(request):
    """
    basic api
    """
    search = request.GET.get("search")
    if "dates" in request.GET:
        dates = request.GET.get("dates").split(",")
    else:
        dates = list(models.Price.objects.values_list(
            "timestamp", flat=True).order_by("timestamp").distinct())[-2:]

    try:
        d1 = arrow.get(dates[0])
        d2 = arrow.get(dates[1])
    except IndexError:
        return HttpResponseBadRequest

    res = models.compare_prices_from_date(d1.isoformat(),
                                          d2.isoformat(),
                                          search=search)

    return HttpResponse(json.dumps(res), content_type="application/json")
