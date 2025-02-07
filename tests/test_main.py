import json
from unittest.mock import patch

from src.main import main_events, main_investment, main_spending_by_category


@patch("requests.get")
@patch("builtins.input", side_effect=["25.11.2021 14:33:34", ""])
def test_main_events(mock_input, mock_get) -> None:
    """ Проверяет работу функции main_events """

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 1},
        "info": {"timestamp": 1738518196, "rate": 98.624849},
        "date": "2025-01-15",
        "result": 98.624849,
    }
    assert json.loads(main_events()) == [
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
             [{'currency': 'USD', 'rate': 98.62},
              {'currency': 'EUR', 'rate': 98.62}],
         'stock_prices':
             [{},
              {}]}
                             ]


@patch("builtins.input", side_effect=["2021 14:33:34", ''])
def test_main_events_wrong_date(mock_input) -> None:
    """ Проверяет работу функции main_events """
    assert json.loads(main_events()) == [{}]


@patch("builtins.input", side_effect=['да', '2021-11', 100])
def test_main_investment(mock_input) -> None:
    """ Проверяет работу функции main_investment """
    assert main_investment() == 9604.96


@patch("builtins.input", side_effect=['нет', '2021-11', 100])
def test_main_investment_answer_no(mock_input) -> None:
    """ Проверяет работу функции main_investment """
    assert main_investment() == 0


@patch("builtins.input", side_effect=['да', 'Госуслуги', '27.12.2021 00:00:00'])
def test_main_spending_by_category(mock_input) -> None:
    """ Проверяет работу функции main_spending_by_category """

    assert json.loads(main_spending_by_category()) == [
        {'MCC': 9402.0,
   'Бонусы (включая кэшбэк)': 2,
   'Валюта операции': 'RUB',
   'Валюта платежа': 'RUB',
   'Дата операции': '24.12.2021 20:02:48',
   'Дата платежа': '25.12.2021',
   'Категория': 'Госуслуги',
   'Кэшбэк': '0',
   'Номер карты': '*7197',
   'Округление на инвесткопилку': 0,
   'Описание': 'Почта России',
   'Статус': 'OK',
   'Сумма операции': -100.2,
   'Сумма операции с округлением': 100.2,
   'Сумма платежа': -100.2},
  {'MCC': 9402.0,
   'Бонусы (включая кэшбэк)': 1,
   'Валюта операции': 'RUB',
   'Валюта платежа': 'RUB',
   'Дата операции': '24.12.2021 19:53:32',
   'Дата платежа': '25.12.2021',
   'Категория': 'Госуслуги',
   'Кэшбэк': '0',
   'Номер карты': '*7197',
   'Округление на инвесткопилку': 0,
   'Описание': 'Почта России',
   'Статус': 'OK',
   'Сумма операции': -78.0,
   'Сумма операции с округлением': 78.0,
   'Сумма платежа': -78.0}
        ]


@patch("builtins.input", side_effect=['да', 'Госуслуги', ''])
def test_main_spending_by_category_no_transactions(mock_input) -> None:
    """ Проверяет работу функции main_spending_by_category """

    assert json.loads(main_spending_by_category()) == [{}]


@patch("builtins.input", side_effect=['да', 'Услуги', '27.12.2021 00:00:00'])
def test_main_spending_by_category_no_category(mock_input) -> None:
    """ Проверяет работу функции main_spending_by_category """

    assert json.loads(main_spending_by_category()) == [{}]


@patch("builtins.input", side_effect=['нет', 'Госуслуги', '27.12.2021 00:00:00'])
def test_main_spending_by_category_answer_no(mock_input) -> None:
    """ Проверяет работу функции main_spending_by_category """

    assert json.loads(main_spending_by_category()) == [{}]