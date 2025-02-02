import datetime
import json
import os
from typing import Dict, List, OrderedDict

import pandas as pd
from pandas import DataFrame
from collections import namedtuple, defaultdict
import pprint
import requests
from dotenv import load_dotenv

from src.external_api import PATH_TO_USER_SETTINGS_FILE
from src.readers import read_json_file, read_excel_file

# Получаю абсолютный путь к корневой директории проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Задаю путь к Excel-файлу с транзакциями
PATH_TO_EXCEL_FILE = os.path.join(BASE_DIR, "data", "operations.xlsx")


def writing_dataframe_to_dict(df_excel_file: DataFrame) -> List[Dict]:
    """
    Считывает финансовые операций из Excel-файла,
    выдаёт объект DataFrame список словарей с транзакциями
    """
    try:
        transactions_dict = df_excel_file.to_dict(orient="records")
    except Exception as error_message:
        print(f"\nВозникла ошибка при записи содержимого Excel-файла в словарь. Текст ошибки: \n{error_message}")
        return [{}]
    if not transactions_dict:
        print("\nВ Excel-файле нет данных")
        return [{}]
    return transactions_dict


def get_date_range(date: str, date_range: str= "M") -> tuple | None:
    """
    Создаёт диапазон дат, к котором просматриваются все операции.
    На вход функции подаются дата, до которой будут рассматриваться операции
    и второй необязательный параметр — диапазон данных. По умолчанию диапазон
    равен одному месяцу (с начала месяца, на который выпадает дата, по саму дату).
    """
    if type(date) is not str:
        print("Неправильная дата")
        return None
    try:
        date_end = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    except Exception as error_message:
        print(f"\n Возникла ошибка при обработке строки даты. Текст ошибки:"
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


# if __name__ == "__main__":
#
#     # print(get_date_range("25.11.2021 14:33:34", 'ALL'))
#     # transactions_list = get_transactions_in_date_range(
#     #     datetime.datetime(2021, 11, 1, 0, 0),
#     #     datetime.datetime(2021, 11, 25, 14, 33, 34))
#     # pprint.pprint(transactions_list, width=40)
#     # pprint.pprint(income_in_date_range(transactions_list), width=40)
#     currencies_and_stocks = read_json_file(PATH_TO_USER_SETTINGS_FILE)
    # pprint.pprint(get_currencies_rate(currencies_and_stocks))
    # pprint.pprint(get_stocks_rate(currencies_and_stocks))

