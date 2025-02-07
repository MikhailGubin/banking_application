from unittest.mock import patch

import pandas as pd
import pytest

from src.services import get_transactions_for_investment, investment_bank


def test_get_transactions_for_investment() -> None:
    """Проверяет работу функции get_transactions_for_investment"""

    assert get_transactions_for_investment()[-3:] == [
        {"Дата операции": "03.01.2018 14:55:21", "Сумма операции": 21.0},
        {"Дата операции": "01.01.2018 20:27:51", "Сумма операции": 316.0},
        {"Дата операции": "01.01.2018 12:49:53", "Сумма операции": 3000.0},
    ]


@patch("pandas.read_excel")
def test_get_transactions_for_investment_empty_data(mock_read) -> None:
    """Проверяет работу функции get_transactions_for_investment"""
    mock_read.return_value = pd.DataFrame({})
    assert get_transactions_for_investment()[-3:] == [{}]


@pytest.mark.parametrize(
    "limit, month, expected",
    [(10, "2021-11", 1054.96), (50, "2021-11", 5154.96), (100, "2021-11", 9604.96), (50, "2021-10", 4940.55)],
)
def test_investment_bank(limit: int, month: str, expected: float) -> None:
    """Проверяет работу функции investment_bank"""
    transactions = get_transactions_for_investment()
    assert investment_bank(month, transactions, limit) == expected


@pytest.mark.parametrize("limit, month", [(40, "2021-11"), (50, 2021 - 11), ("100", "2021-11"), (50, "2021-10-10")])
def test_investment_bank_wrong_data(limit: int, month: str) -> None:
    """
    Проверяет работу функции investment_bank,
    когда на вход переданы неправильные значения
    """
    transactions = get_transactions_for_investment()
    assert investment_bank(month, transactions, limit) == 0


def test_investment_bank_no_operations() -> None:
    """
    Проверяет работу функции investment_bank, когда
    нет банковских операций в данном временном периоде
    """
    month = "2024-11"
    transactions = get_transactions_for_investment()
    limit = 50
    assert investment_bank(month, transactions, limit) == 0
