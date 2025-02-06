import datetime
import pprint
from typing import Optional

import pandas as pd

from src.decorator import log
from src.utils import get_date_range
from src.writer import writing_dataframe_to_dict


@log(filename="spending_by_category")
def spending_by_category(transactions: pd.DataFrame, category_name: str, date: Optional[str] = None)-> list[dict]:
    """
     Возвращает траты по заданной категории за последние 3 месяца от переданной даты.
     Принимает на вход датафрейм с транзакциями, название категории и опциональную дату
    """
    if date is None:
        date_obj = datetime.datetime.now()
        date = date_obj.strftime("%d.%m.%Y %H:%M:%S")

    try:
        start_date, end_date = get_date_range(date, "ALL")
    except Exception as error_message:
        print(f"\nВозникла ошибка при обработке даты. Текст ошибки: {error_message}")
        return [{}]

    start_date = pd.to_datetime(start_date, format="%d.%m.%Y %H:%M:%S")
    end_date = pd.to_datetime(end_date, format="%d.%m.%Y %H:%M:%S")

    if transactions is []:
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
        print(f"\nОшибка при работе с датафреймом. Текст ошибки: {error_text}")
        return [{}]

    banking_operations = writing_dataframe_to_dict(transactions_in_date_range)
    return banking_operations
