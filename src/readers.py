import json

import pandas as pd
from pandas import DataFrame


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


def read_json_file(path: str) -> dict:
    """
    Возвращает список словарей с данными о финансовых транзакциях из
    JSON-файла
    """
    # logger_utils.info("Начало работы функции read_json_file")
    try:
        with open(path) as json_file:

            try:
                user_settings = json.load(json_file)
            except json.JSONDecodeError:
                # logger_utils.error("Невозможно декодировать JSON-данные")
                print("\nНевозможно декодировать JSON-данные")
                return {}

    except FileNotFoundError:
        # logger_utils.error("JSON-файл не найден")
        print("\nФайл не найден")
        return {}

    if not user_settings:
        # logger_utils.error("JSON-файл содержит пустой список")
        print("\nФайл содержит пустой список")
        return {}
    elif type(user_settings) is not dict:
        # logger_utils.error("Тип объекта в JSON-файле не список")
        print("\nТип объекта в файле не список")
        return {}
    # logger_utils.info("Функции read_json_file успешно завершила работу")
    return user_settings
