import datetime
import os


from src.external_api import get_currency_rate, get_stocks_price
from src.processing import get_transactions_in_date_range, expenses_in_date_range, income_in_date_range
from src.readers import read_json_file

# Получаю абсолютный путь к корневой директории проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Задаю путь к JSON-файлу с запросами валют и акций
PATH_TO_USER_SETTINGS_FILE = os.path.join(BASE_DIR, "user_settings.json")


def get_date_range(date: str, date_range: str= "M") -> tuple | None:
    """
    Создаёт диапазон дат, к котором просматриваются все операции.
    На вход функции подаются дата, до которой будут рассматриваться операции
    и второй необязательный параметр — диапазон данных. По умолчанию диапазон
    равен одному месяцу (с начала месяца, на который выпадает дата, по саму дату).
    """
    if type(date) is not str:
        print("\nНеправильная дата")
        return None
    try:
        date_end = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    except Exception as error_message:
        print(f"\nВозникла ошибка при обработке строки даты. Текст ошибки:"
              f"{error_message}")
        return None
    if date_range not in ["M", "W", "Y", "ALL"]:
        print("Неправильные данные для диапазона дат")
        return None

    date_start = date_end
    if date_range == 'W':
        date_start = date_end - datetime.timedelta(date_end.isoweekday()) + datetime.timedelta(days=1)
        date_start = date_start.replace(hour=0, minute=0, second=0, microsecond=0)

    elif date_range == 'M':
        date_start = date_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    elif date_range == 'Y':
        date_start = date_end.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    elif date_range == 'ALL':
        month_date_end = date_end.month
        year_date_end = date_end.year
        if month_date_end < 3:
            date_start = date_end.replace(year=(year_date_end - 1),
                                          month=(month_date_end + 12 - 3),
                                          day=1, hour=0, minute=0, second=0, microsecond=0)
        else:

            date_start = date_end.replace(month=(month_date_end - 3), day=1, hour=0, minute=0, second=0, microsecond=0)

    return date_start, date_end


def get_json_answer(date: str, date_range: str= "M") -> list[dict]:
    """ Возвращает JSON-ответ для модуля views.py """
    try:
        date_start, date_end = get_date_range(date, date_range)
        transactions_list = get_transactions_in_date_range(date_start, date_end)
        expenses_dict = expenses_in_date_range(transactions_list)
        income_dict = income_in_date_range(transactions_list)

        user_settings = read_json_file(PATH_TO_USER_SETTINGS_FILE)

        currencies_list = []
        for currency in user_settings["user_currencies"]:
            currencies_list.append(get_currency_rate(currency))

        stocks_list = []
        for stock in user_settings["user_stocks"]:
            stocks_list.append(get_stocks_price(stock))

        json_answer = {"expenses": expenses_dict, "income": income_dict, "currency_rates": currencies_list,
                       "stock_prices": stocks_list}
    except Exception as error_message:
        print(f"Возникла ошибка. Текст ошибки: \n{error_message}")
        return [{}]
    if json_answer == {}:
        print("Нет данных")
        return [{}]
    return [json_answer]


if __name__ == "__main__":
    print(get_json_answer("25.11.2021 14:33:34", "M"))