import datetime
import calendar
import logging
import os
from typing import List, Dict, Any

from src.processing import PATH_TO_EXCEL_FILE, BASE_DIR
from src.readers import read_excel_file
from src.writer import writing_dataframe_to_dict


# Задаю путь к файлу utils.log в директории logs
LOG_PATH = os.path.join(BASE_DIR, "logs", "utils.log")


logger_utils = logging.getLogger(__name__)
file_handler_utils = logging.FileHandler(LOG_PATH, mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler_utils.setFormatter(file_formatter)
logger_utils.addHandler(file_handler_utils)
logger_utils.setLevel(logging.DEBUG)


def get_transactions_for_investment() -> List[Dict[str, Any]]:
    """
    Возвращает список транзакций для работы функции investment_bank
    Пример выходных данных:
    transactions = [{"Дата операции": 'YYYY-MM-DD', "Сумма операции": 4000}, ...]
    """

    df_banking_operations = read_excel_file(PATH_TO_EXCEL_FILE)
    operations_dict = writing_dataframe_to_dict(df_banking_operations)

    transactions_list = []
    for operation in operations_dict:
        if 'Дата операции' not in operation:
            continue
        elif 'Категория' not in operation or not operation['Категория']:
            operation['Категория'] = "Неизвестная категория"
        elif 'Сумма платежа' not in operation:
            continue
        elif type(operation['Сумма платежа']) is not float:
            continue

        if operation['Сумма платежа'] < 0:
            transactions_list.append(
                {'Дата операции': operation['Дата операции'],
                 'Сумма операции': round(abs(operation['Сумма платежа']), 2)}
                            )

    if not transactions_list:
        print("\nВ данном диапазоне времени нет транзакций, удовлетворяющих условиям поиска")
        return [{}]

    return transactions_list


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Возвращает сумму, которую удалось бы отложить в "Инвесткопилку".
    month - месяц, для которого рассчитывается отложенная сумма, строка в формате 'YYYY-MM'
    """
    if type(month) is not str:
        print("\nНеправильный формат параметра 'month'")
        return 0
    if type(limit) is not int:
        print("\nНеправильный формат параметра 'limit'")
        return 0
    elif limit not in [10, 50, 100]:
        print("\nНеправильные данные для параметра 'limit'")
        return 0

    try:
        start_date = datetime.datetime.strptime(month, "%Y-%m")
    except Exception as error_message:
        print(f"\n Возникла ошибка при обработке строки даты. Текст ошибки:"
              f"{error_message}")
        return 0
    last_day = calendar.monthrange(start_date.year, start_date.month)[1]
    end_date = start_date.replace(day=last_day)

    invest = 0
    for transaction in transactions:
        try:
            transaction_date = datetime.datetime.strptime(transaction['Дата операции'], "%d.%m.%Y %H:%M:%S")
        except Exception as error_message:
            print("\nНеправильный формат даты в списке транзакций")
            continue
        if start_date <= transaction_date <= end_date:
            price = transaction["Сумма операции"]
            invest += limit - (price%limit)

    if invest == 0:
        print("\nВ 'Инвесткопилку' не удалось ничего отложить в данном месяце")
        return 0
    return round(invest, 2)

if __name__ == "__main__":

    month = '2021-2'
    # date = datetime.datetime.strptime(month, "%Y-%m")
    # print(datetime.datetime.strptime(month, "%Y-%m"))
    print(get_transactions_for_investment())
