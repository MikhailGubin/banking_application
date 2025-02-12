import json
from typing import Optional

import pandas as pd
import pytest

from src.processing import PATH_TO_EXCEL_FILE
from src.readers import read_excel_file
from src.reports import spending_by_category


def test_spending_by_category() -> None:
    """Проверяет работу функции spending_by_category"""
    df_transactions = read_excel_file(PATH_TO_EXCEL_FILE)
    assert json.loads(spending_by_category(df_transactions, "Госуслуги", "27.12.2021 00:00:00")) == [
        {
            "MCC": 9402.0,
            "Бонусы (включая кэшбэк)": 2,
            "Валюта операции": "RUB",
            "Валюта платежа": "RUB",
            "Дата операции": "24.12.2021 20:02:48",
            "Дата платежа": "25.12.2021",
            "Категория": "Госуслуги",
            "Кэшбэк": "0",
            "Номер карты": "*7197",
            "Округление на инвесткопилку": 0,
            "Описание": "Почта России",
            "Статус": "OK",
            "Сумма операции": -100.2,
            "Сумма операции с округлением": 100.2,
            "Сумма платежа": -100.2,
        },
        {
            "MCC": 9402.0,
            "Бонусы (включая кэшбэк)": 1,
            "Валюта операции": "RUB",
            "Валюта платежа": "RUB",
            "Дата операции": "24.12.2021 19:53:32",
            "Дата платежа": "25.12.2021",
            "Категория": "Госуслуги",
            "Кэшбэк": "0",
            "Номер карты": "*7197",
            "Округление на инвесткопилку": 0,
            "Описание": "Почта России",
            "Статус": "OK",
            "Сумма операции": -78.0,
            "Сумма операции с округлением": 78.0,
            "Сумма платежа": -78.0,
        },
    ]


@pytest.mark.parametrize(
    "category_name, date",
    [
        ("Мороженное", "27.12.2021 00:00:00"),
        ("Госуслуги", "12.2021 00:00:00"),
        ("Госуслуги", None),
        ("Госуслуги", 12.2021),
    ],
)
def test_spending_by_category_wrong_date_or_category(category_name: str, date: Optional[str]) -> None:
    """
    Проверяет работу функции spending_by_category,
    когда на вход переданы неправильные данные
    или отсутствуют транзакции
    """
    df_transactions = read_excel_file(PATH_TO_EXCEL_FILE)
    assert json.loads(spending_by_category(df_transactions, category_name, date)) == [{}]


@pytest.mark.parametrize(
    "transactions",
    [
        (pd.DataFrame({"Yes": [50, 131], "No": [21, 2]})),
        ({}),
        (pd.DataFrame({})),
        (pd.DataFrame({"Категория": ["Госуслуги", "Госуслуги"], "Сумма платежа": [212, 560]})),
        (pd.DataFrame({"Дата операции": ["24.12.2021 19:53:32", "24.12.2021 20:02:48"], "Сумма платежа": [212, 560]})),
    ],
)
def test_spending_by_category_empty_df(transactions: any) -> None:
    """
    Проверяет работу функции spending_by_category,
    когда отсутствуют датафрейм с транзакциями
    """
    assert json.loads(spending_by_category(transactions, "Госуслуги", "27.12.2021 00:00:00")) == [{}]
