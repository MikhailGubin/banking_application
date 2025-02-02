from collections import defaultdict
from datetime import datetime

from src.readers import read_excel_file
from src.utils import PATH_TO_EXCEL_FILE, writing_dataframe_to_dict


def get_transactions_in_date_range(date_start: datetime.datetime,
                                  date_end: datetime.datetime) -> list[dict]:
    """
    Принимает дату начала и дата окончания временного интервала для транзакций.
    Возвращает список транзакций с двумя словарями: словарь расходов и словарь поступлений
    """
    df_banking_operations = read_excel_file(PATH_TO_EXCEL_FILE)
    operations_dict = writing_dataframe_to_dict(df_banking_operations)


    transactions_dict = defaultdict(list)
    for operation in operations_dict:
        if 'Дата операции' not in operation:
            continue
        if 'Категория' not in operation:
            operation['Категория'] = "Неизвестная категория"
        if 'Сумма платежа' not in operation:
            continue
        transaction_date = datetime.datetime.strptime(operation['Дата операции'], "%d.%m.%Y %H:%M:%S")
        if date_start < transaction_date < date_end:
            transactions_dict[operation['Категория']].append(operation['Сумма платежа'])

    if not transactions_dict:
        print("В данном диапазоне времени нет транзакций, удовлетворяющих условиям поиска")
        return [{}]
    # Складываю суммы операций по категориям
    category_dict = defaultdict(float)
    for category, amount in transactions_dict.items():
        category_dict[category] = round(sum(amount))

    income_dict = defaultdict(int)
    expenses_dict = defaultdict(int)

    for category, amount in category_dict.items():
        if amount > 0:
            income_dict[category] = amount
        elif amount < 0:
            expenses_dict[category] = amount
    transactions_list = [expenses_dict, income_dict]
    return transactions_list

def expenses_in_date_range(transactions_list: list[dict]) -> dict:
    """
    Принимает на вход список транзакций с двумя словарями:
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
    result_expenses_dict = {
        "total_amount": total_amount,
        "main": expenses_main_list,
        "transfers_and_cash": transfers_and_cash_list
                                         }
    return result_expenses_dict


def income_in_date_range(transactions_list: list[dict]) -> dict:
    """
    Принимает на вход список транзакций с двумя словарями:
    словарь расходов и словарь поступлений.
    Возвращает словарь с поступлениями за указанный период
    """
    all_income = defaultdict(int)
    _, all_income = transactions_list
    # Посчитал общую стоимость расходов за заданный период
    all_income_tuple = all_income.items()
    total_amount = sum([expense[1]
                        for expense in all_income_tuple])

    # Выделяю семь популярных категорий
    income_transactions_sorted = sorted(all_income_tuple,
                                   key=lambda transaction: transaction[1]
                                   )

    # Создаю список для ключа "main" в итоговом словаре поступлений
    income_main_list = [{"category": category, "amount": abs(amount)}
                          for category, amount in income_transactions_sorted]

    # Создаю итоговый словарь трат для формирования JSON- ответа
    result_income_dict = {
        "total_amount": total_amount,
        "main": income_main_list
            }

    return result_income_dict