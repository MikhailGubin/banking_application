from unittest.mock import patch

import pytest

from src.external_api import BASE_URL, get_currency_rate, get_stocks_price


@patch("requests.get")
def test_get_currency_rate(mock_get, data_for_test_get_currency_rate: tuple) -> None:
    """
    Проверяет работу функции get_currency_rate
    при конвертации валюты из долларов в рубли
    """
    # Функция data_for_test_get_currency_rate находится в модуле conftest.py
    headers, params = data_for_test_get_currency_rate

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 1},
        "info": {"timestamp": 1738518196, "rate": 98.624849},
        "date": "2025-01-15",
        "result": 98.624849,
    }

    assert get_currency_rate("USD") == {"currency": "USD", "rate": 98.62}
    mock_get.assert_called_once_with(BASE_URL, headers=headers, params=params)


def test_get_currency_rate_failed_request(data_for_test_get_currency_rate: tuple) -> None:
    """
    Проверяет работу функции get_currency_rate при неправильном запросе к API
    """
    # Функция data_for_test_get_currency_rate находится в модуле conftest.py
    headers, params = data_for_test_get_currency_rate

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 400
        assert get_currency_rate("USD") == {}
        mock_get.assert_called_once_with(BASE_URL, headers=headers, params=params)


@pytest.mark.parametrize("wrong_http_answer", {"result": ""})
def test_get_currency_rate_wrong_api_answer(data_for_test_get_currency_rate: tuple, wrong_http_answer: any) -> None:
    """
    Проверяет работу функции get_currency_rate,
    если полученный ответ от сервера не является корректным
    HTTP-ответом
    """
    # Функция data_for_test_get_currency_rate находится в модуле conftest.py
    headers, params = data_for_test_get_currency_rate

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = wrong_http_answer
        assert get_currency_rate("USD") == {}
        mock_get.assert_called_once_with(BASE_URL, headers=headers, params=params)


def test_get_stocks_price(data_for_test_get_stocks_price: tuple) -> None:
    """
    Проверяет работу функции get_stocks_price
    при конвертации валюты из долларов в рубли
    """
    # Функция data_for_test_get_stocks_price находится в модуле conftest.py
    apikey_stock = data_for_test_get_stocks_price
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "meta": {
                "currency": "USD",
                "exchange": "NASDAQ",
                "exchange_timezone": "America/New_York",
                "interval": "1h",
                "mic_code": "XNGS",
                "symbol": "AAPL",
                "type": "Common Stock",
            },
            "status": "ok",
            "values": [
                {
                    "close": "228.31",
                    "datetime": "2025-02-03 14:30:00",
                    "high": "228.52",
                    "low": "228.31",
                    "open": "228.48",
                    "volume": "6138",
                },
                {
                    "close": "228.41",
                    "datetime": "2025-02-03 13:30:00",
                    "high": "228.825",
                    "low": "226.895",
                    "open": "226.91",
                    "volume": "207801",
                },
            ],
        }

        assert get_stocks_price("APPL") == {"stock": "APPL", "price": 228.31}
        mock_get.assert_called_once_with(
            f"https://api.twelvedata.com/time_series?symbol=APPL&interval=1h&" f"apikey={apikey_stock}"
        )


def test_get_stocks_price_failed_request(data_for_test_get_stocks_price: tuple) -> None:
    """
    Проверяет работу функции get_currency_rate при неправильном запросе к API
    """
    # Функция data_for_test_get_stocks_price находится в модуле conftest.py
    apikey_stock = data_for_test_get_stocks_price

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 400
        assert get_stocks_price("APPL") == {}
        mock_get.assert_called_once_with(
            f"https://api.twelvedata.com/time_series?symbol=APPL&interval=1h&" f"apikey={apikey_stock}"
        )


@pytest.mark.parametrize("wrong_http_answer", {"values": [{"close": ""}]})
def test_get_stocks_price_wrong_api_answer(data_for_test_get_stocks_price: tuple, wrong_http_answer: any) -> None:
    """
    Проверяет работу функции get_currency_rate,
    если полученный ответ от сервера не является корректным
    HTTP-ответом
    """
    # Функция data_for_test_get_stocks_price находится в модуле conftest.py
    apikey_stock = data_for_test_get_stocks_price

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = wrong_http_answer
        assert get_stocks_price("APPL") == {}
        mock_get.assert_called_once_with(
            f"https://api.twelvedata.com/time_series?symbol=APPL&interval=1h&" f"apikey={apikey_stock}"
        )
