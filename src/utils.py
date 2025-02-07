import datetime
import json
import logging
import os
from typing import Any

from src.external_api import get_currency_rate, get_stocks_price
from src.processing import expenses_in_date_range, get_transactions_in_date_range, income_in_date_range
from src.readers import read_json_file

# Получаю абсолютный путь к корневой директории проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Задаю путь к JSON-файлу с запросами валют и акций
PATH_TO_USER_SETTINGS_FILE = os.path.join(BASE_DIR, "user_settings.json")
# Задаю путь к файлу utils.log в директории logs
LOG_PATH_UTILS = os.path.join(BASE_DIR, "data", "utils.log")


logger_utils = logging.getLogger(__name__)
file_handler_utils = logging.FileHandler(LOG_PATH_UTILS, mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler_utils.setFormatter(file_formatter)
logger_utils.addHandler(file_handler_utils)
logger_utils.setLevel(logging.DEBUG)


def get_date_range(date: str, date_range: str = "M") -> tuple | None:
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
        print(f"\nВозникла ошибка при обработке строки даты. Текст ошибки:" f"{error_message}")
        return None
    if date_range not in ["M", "W", "Y", "ALL"]:
        print("Неправильные данные для диапазона дат")
        return None

    date_start = date_end
    if date_range == "W":
        date_start = date_end - datetime.timedelta(date_end.isoweekday()) + datetime.timedelta(days=1)
        date_start = date_start.replace(hour=0, minute=0, second=0, microsecond=0)

    elif date_range == "M":
        date_start = date_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    elif date_range == "Y":
        date_start = date_end.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    elif date_range == "ALL":
        day_date_end = date_end.day
        month_date_end = date_end.month
        year_date_end = date_end.year
        if month_date_end < 3:
            date_start = date_end.replace(
                year=(year_date_end - 1),
                month=(month_date_end + 12 - 3),
                day=day_date_end,
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
        else:

            date_start = date_end.replace(
                month=(month_date_end - 3), day=day_date_end, hour=0, minute=0, second=0, microsecond=0
            )

    return date_start, date_end


def get_json_answer(date: str, date_range: str = "M") -> list[dict[Any, Any]] | str:
    """Возвращает JSON-ответ для модуля views.py"""
    logger_utils.info("Начало работы приложения 'События'")
    try:
        date_start, date_end = get_date_range(date, date_range)
        logger_utils.info("Окончание работы функции работы функции get_date_range")

        transactions_list = get_transactions_in_date_range(date_start, date_end)
        logger_utils.info("Окончание работы функции работы функции get_transactions_in_date_range")

        expenses_dict = expenses_in_date_range(transactions_list)
        logger_utils.info("Окончание работы функции работы функции expenses_in_date_range")

        income_dict = income_in_date_range(transactions_list)
        logger_utils.info("Окончание работы функции работы функции income_in_date_range")

        user_settings = read_json_file(PATH_TO_USER_SETTINGS_FILE)
        logger_utils.info("Окончание работы функции работы функции read_json_file")

        currencies_list = []
        for currency in user_settings["user_currencies"]:
            currencies_list.append(get_currency_rate(currency))

        stocks_list = []
        for stock in user_settings["user_stocks"]:
            stocks_list.append(get_stocks_price(stock))

        result = [
            {
                "expenses": expenses_dict,
                "income": income_dict,
                "currency_rates": currencies_list,
                "stock_prices": stocks_list,
            }
        ]
    except Exception as error_message:
        logger_utils.error(f"Возникла ошибка. Текст ошибки: \n{error_message}")
        print(f"\nВозникла ошибка. Текст ошибки: \n{error_message}")
        return json.dumps([{}])

    if result == [{}]:
        logger_utils.info("Нет данных в ответе от приложения 'События'")
        print("Нет данных в ответе от приложения 'События'")
        return json.dumps([{}])

    json_answer = json.dumps(result)
    logger_utils.info("Успешное окончание работы приложения 'События'")
    return json_answer
