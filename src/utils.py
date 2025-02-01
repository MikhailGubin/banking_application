import datetime
import json
import os
from typing import Dict, List

import pandas as pd
from pandas import DataFrame
from collections import namedtuple, defaultdict
import pprint

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

def get_transactions_in_date_range(date_start: datetime.datetime,
                                  date_end: datetime.datetime) -> list[dict]:
    """
    Принимает дату начала и дата окончания временного интервала для транзакций.
    Возвращает список транзакций с двумя словарями: словарь расходов и словарь поступлений
    """
    df_banking_operations = read_excel_file(PATH_TO_EXCEL_FILE)
    operations_dict = writing_dataframe_to_dict(df_banking_operations)


    transactions_dict = defaultdict(list)
    for transaction in operations_dict:
        transaction_date = datetime.datetime.strptime(transaction['Дата операции'], "%d.%m.%Y %H:%M:%S")
        if date_start < transaction_date < date_end:
            transactions_dict[transaction['Категория']].append(transaction['Сумма платежа'])


    # Складываю суммы операций по категориям
    category_dict = defaultdict(float)
    for category, amount in transactions_dict.items():
        category_dict[category] = round(sum(amount))

    income_dict = defaultdict(int)
    expenses_dict = defaultdict(int)
    # income_list = [(category, amount)
    #                for category, amount in category_dict
    #                if amount >0]

    for category, amount in category_dict.items():
        if amount > 0:
            income_dict[category] = amount
        elif amount < 0:
            expenses_dict[category] = amount
    transactions_list = [expenses_dict, income_dict]
    return transactions_list

def expenses_in_date_range(transactions_list: list[dict]) -> list[dict]:
    """"
    Принимает на вход список транзакций список транзакций с двумя словарями:
    словарь расходов и словарь поступлений.
    Возвращает словарь с расходами за указанный период
    """
    all_expenses = defaultdict(int)
    all_expenses, _ = transactions_list
    # Посчитал общую стоимость расходов за заданный период
    all_expenses_tuple = all_expenses.items()
    total_amount = sum([expense[1]
                        for expense in all_expenses_tuple])

    # Выделяю семь популярных категорий
    most_popular_expenses = sorted(all_expenses_tuple,
                                   key=lambda operation: operation[1]
                                   )[0:7]

    # Вычисляю стоимость семи популярных категорий трат
    most_popular_expenses_amount = sum([expense[1]
                        for expense in most_popular_expenses])

    # Вычисляю стоимость остальных категорий трат
    others_amount = total_amount - most_popular_expenses_amount
    most_popular_expenses.append(("Остальное", others_amount))

    #Создаю список для ключа "main" в итоговом словаре трат
    expenses_main_list = [{"category": category, "amount": abs(amount)}
                          for category, amount in most_popular_expenses]

    cash_amount = all_expenses["Наличные"]
    transfers_amount = abs(all_expenses["Переводы"])

    if cash_amount > transfers_amount:
        transfers_and_cash_list = [
            {"category": "Наличные", "amount": abs(cash_amount)},
            {"category": "Переводы", "amount": abs(transfers_amount)}
                                   ]
    else:
        transfers_and_cash_list = [
            {"category": "Переводы", "amount": abs(transfers_amount)},
            {"category": "Наличные", "amount": abs(cash_amount)}
                                   ]

    # Создаю итоговый словарь трат для формирования JSON- ответа
    result_expenses_dict = {"expenses": {
        "total_amount": total_amount,
        "main": expenses_main_list,
        "transfers_and_cash": transfers_and_cash_list
                                         }}
    return result_expenses_dict



if __name__ == "__main__":

    # print(get_date_range("25.11.2021 14:33:34", 'ALL'))

    transactions_list = get_transactions_in_date_range(
        datetime.datetime(2021, 11, 1, 0, 0),
        datetime.datetime(2021, 11, 25, 14, 33, 34))
    # pprint.pprint(transactions_list, width=40)
    pprint.pprint(expenses_in_date_range(transactions_list), width=40)

