import os

import pytest
from dotenv import load_dotenv


@pytest.fixture
def data_for_test_get_currency_rate() -> tuple:
    """Возвращает данные для теста функции test_get_currency_rate"""
    load_dotenv()
    apikey = os.getenv("API_KEY")
    headers = {"apikey": f"{apikey}"}
    params = {"to": "RUB", "from": "USD", "amount": 1}
    return headers, params


@pytest.fixture
def data_for_test_get_stocks_price() -> str:
    """Возвращает данные для теста функции test_get_stocks_price"""
    load_dotenv()
    apikey_stock = os.getenv("API_KEY_TWELVE_DATA")
    return apikey_stock
