from unittest.mock import patch
from unittest.mock import MagicMock

import pytest
from django.db.models import QuerySet

from card import models


@patch('card.models.Price')
def test_compare_prices(MockPrice):
    """
    Test compare_prices_from_date
    """
    date1 = '2019-05-09T00:00:00+00:00'
    date2 = '2019-06-07T00:00:00+00:00'

    def side_effect(timestamp):
        """
        allow dynamic return value
        """
        if date1 == timestamp:
            mock_price = MagicMock(spec=models.Price)
            mock_price.value = 5
            mock_price.card_id = 5
            mock_qs = MagicMock(spec=QuerySet)
            mock_qs.order_by.return_value = [mock_price, ]
            return mock_qs
        else:
            mock_price2 = MagicMock(spec=models.Price)
            mock_price2.value = 300
            mock_price2.card_id = 5
            return [mock_price2, ]

    MockPrice.objects.filter.side_effect = side_effect

    cols = models.compare_prices_from_date(date1, date2)

    assert cols
