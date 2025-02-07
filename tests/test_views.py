import json
from unittest.mock import patch

import pytest

from src.views import events


@patch("requests.get")
def test_events(mock_get) -> None:
    """Проверяет работу функции events"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 1},
        "info": {"timestamp": 1738518196, "rate": 98.624849},
        "date": "2025-01-15",
        "result": 98.624849,
    }

    assert json.loads(events("25.11.2021 14:33:34", "M")) == [
        {
            "expenses": {
                "total_amount": -53700,
                "main": [
                    {"category": "ЖКХ", "amount": 12099},
                    {"category": "Супермаркеты", "amount": 11000},
                    {"category": "Медицина", "amount": 7240},
                    {"category": "Каршеринг", "amount": 6258},
                    {"category": "Фастфуд", "amount": 3566},
                    {"category": "Местный транспорт", "amount": 2712},
                    {"category": "Аптеки", "amount": 2314},
                    {"category": "Остальное", "amount": 8511},
                ],
                "transfers_and_cash": [
                    {"category": "Переводы", "amount": 2000},
                    {"category": "Наличные", "amount": 0},
                ],
            },
            "income": {
                "total_amount": 2896,
                "main": [
                    {"category": "Пополнения", "amount": 200},
                    {"category": "Другое", "amount": 1086},
                    {"category": "Бонусы", "amount": 1610},
                ],
            },
            "currency_rates": [{"currency": "USD", "rate": 98.62}, {"currency": "EUR", "rate": 98.62}],
            "stock_prices": [{}, {}],
        }
    ]


@pytest.mark.parametrize("date, date_range", [(123, "M"), ("string", "ALL"), ("25.01.2021 14:33:34", "A")])
def test_get_json_answer_wrong_data(date: str, date_range: str) -> None:
    """
    Проверяю работу функции get_json_answer, когда на вход
    передаются неверные данные
    """
    assert json.loads(events(date, date_range)) == [{}]
