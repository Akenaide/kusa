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

    def side_effect(timestamp__value):
        """
        allow dynamic return value
        """
        if date1 == timestamp__value:
            mock_price = MagicMock()
            mock_price.return_value = [{"card_id": 5, "value": 5}, ]
            values = MagicMock(**{"values.return_value": [{"card_id": 5, "value": 5}, ]})
            order = MagicMock(**{"order_by.return_value": values})
            mock_price.select_related.return_value = order
            return mock_price
        else:
            mock_price2 = MagicMock(spec=models.Price)
            mock_price2.value = 300
            mock_price2.card_id = 5
            mock_qs = MagicMock(spec=QuerySet)
            mock_qs.only.return_value = [mock_price2, ]
            return mock_qs

    MockPrice.objects.filter.side_effect = side_effect

    cols = models.compare_prices_from_date(date1, date2)

    assert cols
