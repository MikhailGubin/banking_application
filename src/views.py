import datetime

from pandas import DataFrame

from src.utils import PATH_TO_EXCEL_FILE, read_excel_file, writing_dataframe_to_dict
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
    date_end = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    # date_now = datetime.datetime.now()
    if date_range == 'W':
        date_start = date_end - datetime.timedelta(date_now.isoweekday()) + datetime.timedelta(days=1)
        date_start = date_start.replace(hour=0, minute=0, second=0, microsecond=0)

    elif date_range == 'M':
        date_start = date_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    elif date_range == 'Y':
        date_start = date_end.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    elif date_range == 'ALL':
        date_start = date_end.replace(year=1900)

    df_banking_operations = read_excel_file(PATH_TO_EXCEL_FILE)
    operations_dict = writing_dataframe_to_dict(df_banking_operations)

    transactions_list = []
    for transaction in operations_dict:
        transaction_date = datetime.datetime.strptime(transaction['Дата операции'], "%d.%m.%Y %H:%M:%S")
        if date_start < transaction_date < date_end:
            transactions_list.append(transaction)
    total_amount = round(
        sum(
            abs(transaction['Сумма платежа'])
        for transaction in transactions_list
                        if transaction['Сумма платежа'] < 0
            ),
                         0)
    counted_operations = Counter(
        transaction['Категория']
        for transaction in transactions_list
        if transaction['Сумма платежа'] < 0
    )
    popular_operations = [operation[0] for operation in counted_operations.most_common(7)]


    all_data_on_operations = defaultdict(list)
    # all_data_n_operations = {"expenses": {"total_amount": total_amount, "main": []}}
    popular_transactions_dict = defaultdict(list)
    for transaction in transactions_list:
        if transaction['Категория'] in popular_operations:
            # all_data_n_operations["expenses"]["main"].append({"category": transaction['Категория'],
            #                                "amount": round(abs(transaction['Сумма платежа']), 0)})
            # all_data_n_operations["expenses"]["main"]["amount"] = round(abs(transaction['Сумма платежа']), 0)
            popular_transactions_dict[transaction['Категория']] += round(abs(transaction['Сумма платежа']), 0)


    return popular_transactions_dict
if __name__ == "__main__":
    date_now = datetime.datetime.now()
    # print(date_now.isoweekday())
    # date_start = date_now - datetime.timedelta(date_now.isoweekday())+ datetime.timedelta(days=1)
    # date_start = date_start.replace(hour=0, minute=0, second=0, microsecond=0)
    # date_start = date_now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    # print(date_start)
    print(events("05.11.2021 14:33:34"))
