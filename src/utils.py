import json
import os
from typing import Dict, List
from unittest.mock import patch

import pandas as pd
from pandas import DataFrame
from collections import namedtuple

# Получаю абсолютный путь к корневой директории проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Задаю путь к CSV-файлу с транзакциями
PATH_TO_EXCEL_FILE = os.path.join(BASE_DIR, "data", "operations.xlsx")

def read_excel_file(path_to_file: str) -> DataFrame | None:
    """
    Считывает финансовые операций из Excel-файла,
    выдаёт объект DataFrame список словарей с транзакциями
    """

    try:
        df_excel_file = pd.read_excel(path_to_file)
        # Заменяю nan на None
        df_banking_operations = df_excel_file.where(pd.notnull(df_excel_file), None)
    except Exception as error_message:
        print(f"\nВозникла ошибка при чтении Excel-файла. Текст ошибки: \n{error_message}")
        return []

    return df_banking_operations

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


# def user_request() -> dict:
#     """
#     Задаёт валюты и акции для отображения на веб-страницах и записывает в файл пользовательских настроек
#     user_settings.json
#     """
#     curriencies = input('Введите названия интересующих Вас валют')
#     stocks = input('Введите названия интересующих Вас акций')
#     # user_settings = {
#     #     "user_currencies": ["USD", "EUR"],
#     #  "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
#     # }
#     curriencies_list = curriencies.split()
#     stocks_list = stocks.split()
#
#
#     user_settings = {"user_currencies": f"{curriencies_list}", "user_stocks": f"{stocks_list}"}
#     return user_settings
#     # return json.loads(user_settings)

if __name__ == "__main__":
    print(user_request())
    # a = json.loads('{"user_currencies": ["USD", "EUR"], '
    #                '"user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}')
    # print(a)