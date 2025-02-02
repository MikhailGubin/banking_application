import datetime

import pytest

from src.processing import get_transactions_in_date_range


def test_get_transactions_in_date_range() -> None:
    """ Проверяет работу функции def get_transactions_in_date_range"""
    date_start = datetime.datetime(2021, 11, 1, 0, 0)
    date_end = datetime.datetime(2021, 11, 5, 14, 33, 34)

    assert get_transactions_in_date_range(date_start, date_end) == [{'Каршеринг': -5548,
              'Косметика': -482,
              'Местный транспорт': -60,
              'Связь': -20,
              'Супермаркеты': -2029,
              'Фастфуд': -402},
              {'Другое': 10000}]


@pytest.mark.parametrize(
    "operations, expected", [
    ({'MCC': 5499.0,
   'Валюта операции': 'RUB',
   'Валюта платежа': 'RUB',
   'Дата операции': '03.01.2018 15:03:35',
   'Дата платежа': '04.01.2018',
   'Категория': 'Супермаркеты',
   'Кэшбэк': None,
   'Номер карты': '*7197',
   'Округление на инвесткопилку': 0,
   'Описание': 'Magazin 25',
   'Статус': 'OK',
   }, [{}]),
    ({'MCC': 5499.0,
   'Бонусы (включая кэшбэк)': 1,
   'Валюта операции': 'RUB',
   'Валюта платежа': 'RUB',
   'Дата операции': '03.01.2018 15:03:35',
   'Дата платежа': '04.01.2018',
   'Кэшбэк': None,
   'Номер карты': '*7197',
   'Округление на инвесткопилку': 0,
   'Описание': 'Magazin 25',
   'Статус': 'OK',
   'Сумма операции': -73.06,
   'Сумма операции с округлением': 73.06,
   'Сумма платежа': -73.06}, [{"Неизвестная категория": -73}]),
    ({'MCC': 5499.0,
   'Бонусы (включая кэшбэк)': 1,
   'Валюта операции': 'RUB',
   'Валюта платежа': 'RUB',
   'Категория': 'Супермаркеты',
   'Кэшбэк': None,
   'Номер карты': '*7197',
   'Округление на инвесткопилку': 0,
   'Описание': 'Magazin 25',
   'Статус': 'OK',
   'Сумма операции': -73.06,
   'Сумма операции с округлением': 73.06,
   'Сумма платежа': -73.06}, [{}])
        ]
    )
def test_get_transactions_in_date_range_wrong_data(operations: list[dict], expected: list[dict]) -> None:
    """ Проверяет работу функции def get_transactions_in_date_range"""
    date_start = datetime.datetime(2021, 11, 1, 0, 0)
    date_end = datetime.datetime(2021, 11, 5, 14, 33, 34)

    assert get_transactions_in_date_range(date_start, date_end) == expected
