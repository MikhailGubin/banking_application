import datetime
import logging
import os
from typing import Optional

import pandas as pd

from src.decorator import log
from src.utils import get_date_range, BASE_DIR
from src.writer import writing_dataframe_to_dict


# Задаю путь к файлу reports.log в директории logs
LOG_REPORTS_PATH = os.path.join(BASE_DIR, "data", "reports.log")

logger_reports = logging.getLogger(__name__)
file_handler_reports = logging.FileHandler(LOG_REPORTS_PATH, mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler_reports.setFormatter(file_formatter)
logger_reports.addHandler(file_handler_reports)
logger_reports.setLevel(logging.DEBUG)


@log(filename="spending_by_category")
def spending_by_category(transactions: pd.DataFrame, category_name: str, date: Optional[str] = None)-> list[dict]:
    """
     Возвращает траты по заданной категории за последние 3 месяца от переданной даты.
     Принимает на вход датафрейм с транзакциями, название категории и опциональную дату
    """
    logger_reports.info("Приложение 'Траты по категории' начинает работу")
    if date is None:
        logger_reports.info("Дата не выбрана, берется текущая дата.")
        print("Дата не выбрана, берется текущая дата.")
        date_obj = datetime.datetime.now()
        date = date_obj.strftime("%d.%m.%Y %H:%M:%S")

    try:
        start_date, end_date = get_date_range(date, "ALL")
    except Exception as error_message:
        logger_reports.error(f"Возникла ошибка при обработке даты. Текст ошибки: \n{error_message}")
        print(f"\nВозникла ошибка при обработке даты. Текст ошибки: \n{error_message}")
        return [{}]

    start_date = pd.to_datetime(start_date, format="%d.%m.%Y %H:%M:%S")
    end_date = pd.to_datetime(end_date, format="%d.%m.%Y %H:%M:%S")

    if transactions is []:
        logger_reports.error("Пустой датафрейм с транзакциями")
        print("\nПустой датафрейм с транзакциями")
        return [{}]
    try:
        transactions.fillna(value="0", inplace=True)
        transactions_in_date_range = transactions.loc[
        (start_date <= pd.to_datetime(transactions['Дата операции'], format="%d.%m.%Y %H:%M:%S")) &
        (pd.to_datetime(transactions['Дата операции'], format="%d.%m.%Y %H:%M:%S") <= end_date) &
        (transactions['Категория'] == category_name)
                ]
    except Exception as error_text:
        logger_reports.error(f"\nОшибка при работе с датафреймом. Текст ошибки: {error_text}")
        print(f"\nОшибка при работе с датафреймом. Текст ошибки: {error_text}")
        return [{}]

    banking_operations = writing_dataframe_to_dict(transactions_in_date_range)
    logger_reports.info("Приложение 'Траты по категории' успешно закончило работу")
    return banking_operations
