from unittest.mock import patch
from unittest.mock import MagicMock

import pytest

import card.import_prices as ijson
from card.models import Card
from card.models import Price


@pytest.fixture
def first_data():
    return {
        "AB/W11-001": {
            "ID": "AB/W11-001",
            "Translation": "",
            "Amount": 0,
            "URL": "https://yuyu-tei.jp/card_image/ws/front/ab/10025.jpg",
            "Price": 200,
            "YytSetCode": "ab",
            "Rarity": "RR",
            "CardURL": "https://yuyu-tei.jp/game_ws/carddetail/cardpreview.php?VER=ab\u0026CID=10025\u0026MODE=sell",
            "EBFoil": False
        },
        "AB/W11-001SP": {
            "ID": "AB/W11-001SP",
            "Translation": "",
            "Amount": 0,
            "URL": "https://yuyu-tei.jp/card_image/ws/front/ab/10138.jpg",
            "Price": 4980,
            "YytSetCode": "ab",
            "Rarity": "SP",
            "CardURL": "https://yuyu-tei.jp/game_ws/carddetail/cardpreview.php?VER=ab\u0026CID=10138\u0026MODE=sell",
            "EBFoil": False
        },
        "AB/W11-002": {
            "ID": "AB/W11-002",
            "Translation": "",
            "Amount": 0,
            "URL": "https://yuyu-tei.jp/card_image/ws/front/ab/10026.jpg",
            "Price": 150,
            "YytSetCode": "ab",
            "Rarity": "RR",
            "CardURL": "https://yuyu-tei.jp/game_ws/carddetail/cardpreview.php?VER=ab\u0026CID=10026\u0026MODE=sell",
            "EBFoil": False
        },
        "RSL/S56-037SSP": {
            "ID": "RSL/S56-037SSP",
            "Translation": "",
            "Amount": 0,
            "URL": "https://yuyu-tei.jp/card_image/ws/front/rsl/10194.jpg",
            "Price": 14800,
            "YytSetCode": "rsl",
            "Rarity": "SSP",
            "CardURL": "https://yuyu-tei.jp/game_ws/carddetail/cardpreview.php?VER=rsl\u0026CID=10194\u0026MODE=sell",
            "EBFoil": False
        },
        "RSL/S56-038": {
            "ID": "RSL/S56-038",
            "Translation": "",
            "Amount": 0,
            "URL": "https://yuyu-tei.jp/card_image/ws/front/rsl/10088.jpg",
            "Price": 50,
            "YytSetCode": "rsl",
            "Rarity": "R",
            "CardURL": "https://yuyu-tei.jp/game_ws/carddetail/cardpreview.php?VER=rsl\u0026CID=10088\u0026MODE=sell",
            "EBFoil": False
        },
        "RSL/S56-038S": {
            "ID": "RSL/S56-038S",
            "Translation": "",
            "Amount": 0,
            "URL": "https://yuyu-tei.jp/card_image/ws/front/rsl/10161.jpg",
            "Price": 200,
            "YytSetCode": "rsl",
            "Rarity": "SR",
            "CardURL": "https://yuyu-tei.jp/game_ws/carddetail/cardpreview.php?VER=rsl\u0026CID=10161\u0026MODE=sell",
            "EBFoil": False
        },
        "SW/S49-094": {
            "ID": "SW/S49-094",
            "Translation": "",
            "Amount": 0,
            "URL": "https://yuyu-tei.jp/card_image/ws/front/starwars/10119.jpg",
            "Price": 100,
            "YytSetCode": "starwars",
            "Rarity": "R",
            "CardURL": "https://yuyu-tei.jp/game_ws/carddetail/cardpreview.php?VER=starwars\u0026CID=10119\u0026MODE=sell",
            "EBFoil": False
        },
        "SW/S49-095": {
            "ID": "SW/S49-095",
            "Translation": "",
            "Amount": 0,
            "URL": "https://yuyu-tei.jp/card_image/ws/front/starwars/10120.jpg",
            "Price": 50,
            "YytSetCode": "starwars",
            "Rarity": "R",
            "CardURL": "https://yuyu-tei.jp/game_ws/carddetail/cardpreview.php?VER=starwars\u0026CID=10120\u0026MODE=sell",
            "EBFoil": False
        },
    }


@pytest.fixture
def second_data():
    return {
        "AB/W12-001": {
            "ID": "AB/W11-001",
            "Translation": "",
            "Amount": 0,
            "URL": "https://yuyu-tei.jp/card_image/ws/front/ab/10025.jpg",
            "Price": 200,
            "YytSetCode": "ab",
            "Rarity": "RR",
            "CardURL": "https://yuyu-tei.jp/game_ws/carddetail/cardpreview.php?VER=ab\u0026CID=10025\u0026MODE=sell",
            "EBFoil": False
        },
        "AB/W11-001": {
            "ID": "AB/W11-001",
            "Translation": "",
            "Amount": 0,
            "URL": "https://yuyu-tei.jp/card_image/ws/front/ab/10025.jpg",
            "Price": 200,
            "YytSetCode": "ab",
            "Rarity": "RR",
            "CardURL": "https://yuyu-tei.jp/game_ws/carddetail/cardpreview.php?VER=ab\u0026CID=10025\u0026MODE=sell",
            "EBFoil": False
        },
        "AB/W11-001SP": {
            "ID": "AB/W11-001SP",
            "Translation": "",
            "Amount": 0,
            "URL": "https://yuyu-tei.jp/card_image/ws/front/ab/10138.jpg",
            "Price": 4980,
            "YytSetCode": "ab",
            "Rarity": "SP",
            "CardURL": "https://yuyu-tei.jp/game_ws/carddetail/cardpreview.php?VER=ab\u0026CID=10138\u0026MODE=sell",
            "EBFoil": False
        },
        "AB/W11-002": {
            "ID": "AB/W11-002",
            "Translation": "",
            "Amount": 0,
            "URL": "https://yuyu-tei.jp/card_image/ws/front/ab/10026.jpg",
            "Price": 150,
            "YytSetCode": "ab",
            "Rarity": "RR",
            "CardURL": "https://yuyu-tei.jp/game_ws/carddetail/cardpreview.php?VER=ab\u0026CID=10026\u0026MODE=sell",
            "EBFoil": False
        },
        "RSL/S56-037SSP": {
            "ID": "RSL/S56-037SSP",
            "Translation": "",
            "Amount": 0,
            "URL": "https://yuyu-tei.jp/card_image/ws/front/rsl/10194.jpg",
            "Price": 14800,
            "YytSetCode": "rsl",
            "Rarity": "SSP",
            "CardURL": "https://yuyu-tei.jp/game_ws/carddetail/cardpreview.php?VER=rsl\u0026CID=10194\u0026MODE=sell",
            "EBFoil": False
        },
        "RSL/S56-038": {
            "ID": "RSL/S56-038",
            "Translation": "",
            "Amount": 0,
            "URL": "https://yuyu-tei.jp/card_image/ws/front/rsl/10088.jpg",
            "Price": 50,
            "YytSetCode": "rsl",
            "Rarity": "R",
            "CardURL": "https://yuyu-tei.jp/game_ws/carddetail/cardpreview.php?VER=rsl\u0026CID=10088\u0026MODE=sell",
            "EBFoil": False
        },
        "RSL/S56-038S": {
            "ID": "RSL/S56-038S",
            "Translation": "",
            "Amount": 0,
            "URL": "https://yuyu-tei.jp/card_image/ws/front/rsl/10161.jpg",
            "Price": 200,
            "YytSetCode": "rsl",
            "Rarity": "SR",
            "CardURL": "https://yuyu-tei.jp/game_ws/carddetail/cardpreview.php?VER=rsl\u0026CID=10161\u0026MODE=sell",
            "EBFoil": False
        },
        "SW/S49-094": {
            "ID": "SW/S49-094",
            "Translation": "",
            "Amount": 0,
            "URL": "https://yuyu-tei.jp/card_image/ws/front/starwars/10119.jpg",
            "Price": 100,
            "YytSetCode": "starwars",
            "Rarity": "R",
            "CardURL": "https://yuyu-tei.jp/game_ws/carddetail/cardpreview.php?VER=starwars\u0026CID=10119\u0026MODE=sell",
            "EBFoil": False
        },
        "SW/S49-095": {
            "ID": "SW/S49-095",
            "Translation": "",
            "Amount": 0,
            "URL": "https://yuyu-tei.jp/card_image/ws/front/starwars/10120.jpg",
            "Price": 50,
            "YytSetCode": "starwars",
            "Rarity": "R",
            "CardURL": "https://yuyu-tei.jp/game_ws/carddetail/cardpreview.php?VER=starwars\u0026CID=10120\u0026MODE=sell",
            "EBFoil": False
        },
    }


@patch('card.import_prices.models')
def test_first_import(MockCard, first_data):
    """
    Test import on empty db
    """

    MockCard.Card.objects.all.return_value.only = lambda x: []

    prices = ijson.parse_prices(first_data, "2019-01-05")

    assert len(prices) == len(first_data)


@patch('card.import_prices.models')
def test_import_new_prices_without_new_cards(MockCard, first_data):
    """
    Test import on not empty db
    """
    mock_card = MagicMock(spec=Card)
    mock_card._state = MagicMock()
    mock_card.card_id = "AB/W11-001"
    MockCard.Card.objects.all.return_value.only = lambda x: [mock_card]
    ijson.parse_prices(first_data, "2019-01-05")
    assert MockCard.Card.objects.create.call_count == 7


@pytest.mark.django_db
def test_import_prices(first_data, second_data):
    """
    Test import price
    """
    ijson.import_prices(first_data, "2019-05-06")
    assert Card.objects.count() == len(first_data)
    ijson.import_prices(second_data, "2019-05-08")
    assert Card.objects.count() == len(second_data)
    assert Price.objects.count() == len(second_data) + len(first_data)
