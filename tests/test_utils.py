import datetime
from typing import Any
from unittest.mock import patch

import pandas as pd
import pytest
from src.utils import get_date_range, get_json_answer


@pytest.mark.parametrize(
    "date, date_range, expected", [
    ("25.11.2021 14:33:34", "M",
     (datetime.datetime(2021, 11, 1, 0, 0),
     datetime.datetime(2021, 11, 25, 14, 33, 34))
     ),
    ("25.11.2021 14:33:34", "ALL",
     (datetime.datetime(2021, 8, 1, 0, 0),
     datetime.datetime(2021, 11, 25, 14, 33, 34))
     ),
        ("25.01.2021 14:33:34", "ALL",
         (datetime.datetime(2020, 10, 1, 0, 0),
          datetime.datetime(2021, 1, 25, 14, 33, 34))
         ),
    ("1.1.2022 14:33:34", "W",
     (datetime.datetime(2021, 12, 27, 0, 0),
     datetime.datetime(2022, 1, 1, 14, 33, 34))
     ),
    ("25.11.2021 14:33:34", "Y",
     (datetime.datetime(2021, 1, 1, 0, 0),
     datetime.datetime(2021, 11, 25, 14, 33, 34))
     )
    ]
)
def test_get_date_range(date: str, date_range: str, expected: tuple) -> None:
    """ Проверяет работу функции get_date_range"""

    assert get_date_range(date, date_range) == expected

@pytest.mark.parametrize(
    "date, date_range", [
    (123, "M"),
    ("string", "ALL"),
    ("25.01.2021 14:33:34", "A")
        ]
    )
def test_get_date_range_wrong_date(date: str, date_range: str) -> None:
    """
    Проверяет работу функции get_date_range,
    сли на вход передана неправильная дата
    """

    assert get_date_range(date, date_range) is None


@patch("requests.get", side_effect=[
        {   "success": True,
            "query": {"from": "USD", "to": "RUB", "amount": 1},
            "info": {"timestamp": 1738518196, "rate": 98.624849},
            "date": "2025-01-15",
            "result": 98.624849,
        },
        {   "success": True,
            "query": {"from": "EUR", "to": "RUB", "amount": 1},
            "info": {"timestamp": 1738518196, "rate": 103.324849},
            "date": "2025-01-15",
            "result": 103.324849,
        },
        {'meta': {'currency': 'USD',
                  'symbol': 'AAPL'},
        'values': [{'close': '232.06'}]
            },
        {'meta': {'currency': 'USD',
                  'symbol': 'AMZN'},
        'values': [{'close': '241.29'}]
            }
        ])
def test_get_json_answer(mock_get) -> None:
    """ Проверяю работу функции get_json_answer"""
    assert get_json_answer("25.11.2021 14:33:34", "M") == [
        {'expenses':
             {'total_amount': -53700,
              'main': [{'category': 'ЖКХ', 'amount': 12099},
                       {'category': 'Супермаркеты', 'amount': 11000},
                       {'category': 'Медицина', 'amount': 7240},
                       {'category': 'Каршеринг', 'amount': 6258},
                       {'category': 'Фастфуд', 'amount': 3566},
                       {'category': 'Местный транспорт', 'amount': 2712},
                       {'category': 'Аптеки', 'amount': 2314},
                       {'category': 'Остальное', 'amount': 8511}],
              'transfers_and_cash': [{'category': 'Переводы', 'amount': 2000},
                                     {'category': 'Наличные', 'amount': 0}]},
         'income':
             {'total_amount': 2896,
              'main': [{'category': 'Пополнения', 'amount': 200},
                       {'category': 'Другое', 'amount': 1086},
                       {'category': 'Бонусы', 'amount': 1610}]},
         'currency_rates':
             [{'currency': 'USD', 'rate': 99.62},
              {'currency': 'EUR', 'rate': 103.32}],
         'stock_prices':
             [{'stock': 'AAPL', 'price': 232.06},
              {'stock': 'AMZN', 'price': 241.29}]}]

@pytest.mark.parametrize(
    "date, date_range", [
    (123, "M"),
    ("string", "ALL"),
    ("25.01.2021 14:33:34", "A")
        ]
    )
def test_get_json_answer_wrong_data(date: str, date_range: str) -> None:
        """
        Проверяю работу функции get_json_answer, когда на вход
        передаются неверные данные
        """
        assert get_json_answer(date, date_range) == [{}]