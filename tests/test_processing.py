import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from src.processing import (
    PATH_TO_EXCEL_FILE,
    expenses_in_date_range,
    get_transactions_in_date_range,
    income_in_date_range
)


def test_get_transactions_in_date_range() -> None:
    """Проверяет работу функции def get_transactions_in_date_range"""
    date_start = datetime.datetime(2021, 11, 1, 0, 0)
    date_end = datetime.datetime(2021, 11, 5, 14, 33, 34)

    assert get_transactions_in_date_range(date_start, date_end) == [
        {
            "Каршеринг": -5548,
            "Косметика": -482,
            "Местный транспорт": -60,
            "Связь": -20,
            "Супермаркеты": -2029,
            "Фастфуд": -402,
        },
        {"Другое": 10000},
    ]


@patch("pandas.read_excel")
def test_get_transactions_in_date_range_wrong_data(mock_read) -> None:
    """
    Проверяет работу функции def get_transactions_in_date_range,
    когда в списке банковских операций отсутствуют нужные ключи
    """
    date_start = datetime.datetime(2021, 11, 1, 0, 0)
    date_end = datetime.datetime(2021, 11, 5, 14, 33, 34)
    mock_read.return_value = pd.DataFrame(
        {
            "Дата операции": ["03.11.2021 15:03:35", "", "03.11.2021 15:03:35"],
            "Категория": ["", "Супермаркеты", "Супермаркеты"],
            "Сумма платежа": [-73.06, -73.06, ""],
        }
    )

    assert get_transactions_in_date_range(date_start, date_end) == [{"Неизвестная категория": -73}, {}]
    mock_read.assert_called_once_with(PATH_TO_EXCEL_FILE)


def test_expenses_in_date_range() -> None:
    """Проверяет работу функции expenses_in_date_range"""
    date_start = datetime.datetime(2021, 11, 1, 0, 0)
    date_end = datetime.datetime(2021, 11, 5, 14, 33, 34)
    transactions_list = get_transactions_in_date_range(date_start, date_end)
    assert expenses_in_date_range(transactions_list) == {
        "total_amount": -8541,
        "main": [
            {"amount": 5548, "category": "Каршеринг"},
            {"amount": 2029, "category": "Супермаркеты"},
            {"amount": 482, "category": "Косметика"},
            {"amount": 402, "category": "Фастфуд"},
            {"amount": 60, "category": "Местный транспорт"},
            {"amount": 20, "category": "Связь"},
            {"amount": 0, "category": "Остальное"},
        ],
        "transfers_and_cash": [{"amount": 0, "category": "Переводы"}, {"amount": 0, "category": "Наличные"}],
    }


@pytest.mark.parametrize(
    "transactions",
    [
        ([]),
        "string",
        ([{}, {"amount": 5548, "category": "Переводы"}]),
        ([{1, 2, 3}, {"amount": 5548, "category": "Переводы"}]),
    ],
)
def test_expenses_in_date_range_wrong_data(transactions: any) -> None:
    """
    Проверяет работу функции expenses_in_date_range,
    когда на вход переданы неправильные данные
    """
    assert expenses_in_date_range(transactions) == {}


def test_income_in_date_range() -> None:
    """Проверяет работу функции income_in_date_range"""
    date_start = datetime.datetime(2021, 11, 1, 0, 0)
    date_end = datetime.datetime(2021, 11, 25, 14, 33, 34)
    transactions_list = get_transactions_in_date_range(date_start, date_end)
    assert income_in_date_range(transactions_list) == {
        "total_amount": 2896,
        "main": [
            {"amount": 200, "category": "Пополнения"},
            {"amount": 1086, "category": "Другое"},
            {"amount": 1610, "category": "Бонусы"},
        ],
    }


@pytest.mark.parametrize(
    "transactions",
    [
        ([]),
        "string",
        ([{"amount": 5548, "category": "Переводы"}, {}]),
        ([{"amount": 5548, "category": "Переводы"}, {1, 2, 3}]),
    ],
)
def test_income_in_date_range_wrong_data(transactions: any) -> None:
    """
    Проверяет работу функции income_in_date_range,
    когда на вход переданы неправильные данные
    """

    assert expenses_in_date_range(transactions) == {}
