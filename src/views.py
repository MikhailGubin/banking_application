import datetime

from pandas import DataFrame

from src.utils import PATH_TO_EXCEL_FILE, read_excel_file, writing_dataframe_to_dict, get_date_range, \
    get_transactions_in_date_range, expenses_in_date_range, income_in_date_range, read_json_file, \
    PATH_TO_USER_SETTINGS_FILE, get_currencies_rate, get_stocks_price
from collections import Counter, defaultdict


def events(date: str, date_range: str= "M") -> dict:
    """
    Реализуйте набор функций и главную функцию, принимающую на вход строку с датой и второй необязательный
    параметр — диапазон данных. По умолчанию диапазон равен одному месяцу (с начала месяца, на который выпадает
    дата, по саму дату). Возможные значения второго необязательного параметра:
    W  — неделя, на которую приходится дата;
    M  — месяц, на который приходится дата;
    Y  — год, на который приходится дата;
    ALL  — все данные до указанной даты.
    Возвращаемый JSON-ответ содержит следующие данные:

    «Расходы»:
    Общая сумма расходов.
    Раздел «Основные», в котором траты по категориям отсортированы по убыванию. Данные предоставляются по 7
    категориям с наибольшими тратами, траты по остальным категориям суммируются и попадают в категорию «Остальное».
    Раздел «Переводы и наличные», в котором сумма по категориям «Наличные» и «Переводы» отсортирована по убыванию.
    «Поступления»:
    Общая сумма поступлений.
    Раздел «Основные», в котором поступления по категориям отсортированы по убыванию.
    Курс валют.
    Стоимость акций из S&P 500."""

    date_start, date_end = get_date_range(date, date_range)
    tansactions_list = get_transactions_in_date_range(date_start, date_end)
    expenses_dict = expenses_in_date_range(tansactions_list)
    income_dict = income_in_date_range(tansactions_list)
    user_settings = read_json_file(PATH_TO_USER_SETTINGS_FILE)
    currencies_rate = get_currencies_rate(user_settings)
    stocks_price = get_stocks_price(user_settings)
    result_dict = defaultdict(list)
    result_dict["expenses"] = expenses_dict
    result_dict["income"] = income_dict
    result_dict["currency_rates"] = currencies_rate
    result_dict["stocks_price"] = stocks_price

    return expenses_dict
if __name__ == "__main__":
    date_now = datetime.datetime.now()
    print(events("25.11.2021 14:33:34"))
