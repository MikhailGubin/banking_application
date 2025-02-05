import pytest

from src.views import events


# def test_events() -> None:
#     """ Проверяет работу функции events """
#
#     assert events("25.11.2021 14:33:34", "M") == [
#         {'expenses':
#              {'total_amount': -53700,
#               'main': [{'category': 'ЖКХ', 'amount': 12099},
#                        {'category': 'Супермаркеты', 'amount': 11000},
#                        {'category': 'Медицина', 'amount': 7240},
#                        {'category': 'Каршеринг', 'amount': 6258},
#                        {'category': 'Фастфуд', 'amount': 3566},
#                        {'category': 'Местный транспорт', 'amount': 2712},
#                        {'category': 'Аптеки', 'amount': 2314},
#                        {'category': 'Остальное', 'amount': 8511}],
#               'transfers_and_cash': [{'category': 'Переводы', 'amount': 2000},
#                                      {'category': 'Наличные', 'amount': 0}]},
#          'income':
#              {'total_amount': 2896,
#               'main': [{'category': 'Пополнения', 'amount': 200},
#                        {'category': 'Другое', 'amount': 1086},
#                        {'category': 'Бонусы', 'amount': 1610}]},
#          'currency_rates':
#              [{'currency': 'USD', 'rate': 99.62},
#               {'currency': 'EUR', 'rate': 103.32}],
#          'stock_prices':
#              [{'stock': 'AAPL', 'price': 232.06},
#               {'stock': 'AMZN', 'price': 241.29}]}]

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
        assert events(date, date_range) == [{}]