from unittest.mock import patch

import pytest

from src.external_api import BASE_URL


def test_get_currencies_rate(currencies_and_stocks: dict) -> None:
    """
    Проверяет работу функции get_amount_of_transaction
    при конвертации валюты из долларов в рубли
    """

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{
            "success": True,
            "query": {"from": "USD", "to": "RUB", "amount": 1},
            "info": {"timestamp": 1737148204, "rate": 102.500986},
            "date": "2025-01-17",
            "result": 102.500986,
        },
            {
                "success": True,
                "query": {"from": "EUR", "to": "RUB", "amount": 1},
                "info": {"timestamp": 1737148204, "rate": 102.500986},
                "date": "2025-01-17",
                "result": 102.500986,
            }
        ]
        # assert test_get_currencies_rate((currencies_and_stocks) == []
        # mock_get.assert_called_once_with(BASE_URL, headers=headers, params=params)


def test_get_amount_of_transaction_eur_to_rub(data_for_test_get_amount_of_transaction: tuple) -> None:
    """
    Проверяет работу функции get_amount_of_transaction
    при конвертации валюты из евро в рубли
    """
    transaction, headers, params = data_for_test_get_amount_of_transaction
    # Функция data_for_test_get_amount_of_transaction находится в модуле conftest.py
    transaction_eur = {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "EUR", "code": "EUR"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }
    params["from"] = "EUR"
    params["amount"] = "1"

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "success": True,
            "query": {"from": "EUR", "to": "RUB", "amount": 9824.07},
            "info": {"timestamp": 1736973004, "rate": 102.502027},
            "date": "2025-01-15",
            "result": 1006987.08839,
        }
        assert test_get_currencies_rate(transaction_eur) == 1006987.09
        mock_get.assert_called_once_with(BASE_URL, headers=headers, params=params)


# def test_get_amount_of_transaction_failed_request(data_for_test_get_amount_of_transaction: tuple) -> None:
#     """
#     Проверяет работу функции get_amount_of_transaction
#     при неправильном запросе к API
#     """
#     transaction, headers, params = data_for_test_get_amount_of_transaction
#     # Функция data_for_test_get_amount_of_transaction находится в модуле conftest.py
#     with patch("requests.get") as mock_get:
#         mock_get.return_value.status_code = 400
#         assert get_amount_of_transaction(transaction) is None
#         mock_get.assert_called_once_with(BASE_URL, headers=headers, params=params)
#
#
# @pytest.mark.parametrize("wrong_http_answer", [{"result": ""}, "string"])
# def test_get_amount_of_transaction_wrong_api_answer(
#     data_for_test_get_amount_of_transaction: tuple, wrong_http_answer: Any
# ) -> None:
#     """
#     Проверяет работу функции get_amount_of_transaction,
#     если полученный ответ от сервера не является корректным
#     HTTP-ответом
#     """
#     transaction, headers, params = data_for_test_get_amount_of_transaction
#     # Функция data_for_test_get_amount_of_transaction находится в модуле conftest.py
#     with patch("requests.get") as mock_get:
#         mock_get.return_value.status_code = 200
#         mock_get.return_value.json.return_value = wrong_http_answer
#         assert get_amount_of_transaction(transaction) is None
#         mock_get.assert_called_once_with(BASE_URL, headers=headers, params=params)
