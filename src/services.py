import calendar
import datetime
import logging
import os
from typing import Any, Dict, List

from src.processing import BASE_DIR, PATH_TO_EXCEL_FILE
from src.readers import read_excel_file
from src.writer import writing_dataframe_to_dict

# Задаю путь к файлу services.log в директории logs
LOG_SERVICES_PATH = os.path.join(BASE_DIR, "data", "services.log")


logger_services = logging.getLogger(__name__)
file_handler_services = logging.FileHandler(LOG_SERVICES_PATH, mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler_services.setFormatter(file_formatter)
logger_services.addHandler(file_handler_services)
logger_services.setLevel(logging.DEBUG)


def get_transactions_for_investment() -> List[Dict[str, Any]]:
    """
    Возвращает список транзакций для работы функции investment_bank
    Пример выходных данных:
    transactions = [{"Дата операции": 'YYYY-MM-DD', "Сумма операции": 4000}, ...]
    """
    # Читаю датафрейм из Excel-файла
    df_banking_operations = read_excel_file(PATH_TO_EXCEL_FILE)
    # Записываю датафрейм в словарь
    operations_dict = writing_dataframe_to_dict(df_banking_operations)
    transactions_list = []
    for operation in operations_dict:
        if "Дата операции" not in operation:
            continue
        elif "Категория" not in operation or not operation["Категория"]:
            operation["Категория"] = "Неизвестная категория"
        elif "Сумма платежа" not in operation:
            continue
        elif type(operation["Сумма платежа"]) is not float:
            continue

        if operation["Сумма платежа"] < 0:
            transactions_list.append(
                {
                    "Дата операции": operation["Дата операции"],
                    "Сумма операции": round(abs(operation["Сумма платежа"]), 2),
                }
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
    logger_services.info("Начало работы сервиса 'Инвесткопилка'")
    if type(month) is not str:
        logger_services.error("Неправильный формат параметра 'month'")
        print("\nНеправильный формат параметра 'month'")
        return 0
    if type(limit) is not int:
        logger_services.error("Неправильный формат параметра 'limit'")
        print("\nНеправильный формат параметра 'limit'")
        return 0
    elif limit not in [10, 50, 100]:
        logger_services.error("Неправильные данные для параметра 'limit'")
        print("\nНеправильные данные для параметра 'limit'")
        return 0

    try:
        start_date = datetime.datetime.strptime(month, "%Y-%m")
    except Exception as error_message:
        logger_services.error(f"Возникла ошибка при обработке строки даты. Текст ошибки:" f"\n{error_message}")
        print(f"\n Возникла ошибка при обработке строки даты. Текст ошибки:" f"\n{error_message}")
        return 0

    last_day = calendar.monthrange(start_date.year, start_date.month)[1]
    end_date = start_date.replace(day=last_day)

    invest = 0
    for transaction in transactions:
        try:
            transaction_date = datetime.datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")
        except Exception as error_message:
            logger_services.error(f"Неправильный формат даты в списке транзакций. \nТекст ошибки: {error_message}")
            print(f"\nНеправильный формат даты в списке транзакций. \nТекст ошибки: {error_message}")
            continue
        if start_date <= transaction_date <= end_date:
            price = transaction["Сумма операции"]
            invest += limit - (price % limit)

    if invest == 0:
        logger_services.info("В 'Инвесткопилку' не удалось ничего отложить в данном месяце")
        print("\nВ 'Инвесткопилку' не удалось ничего отложить в данном месяце")
        return 0
    logger_services.info("Сервис 'Инвесткопилка' успешно завершил работу")
    return round(invest, 2)
