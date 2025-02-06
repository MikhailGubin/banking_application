from src.processing import PATH_TO_EXCEL_FILE
from src.readers import read_excel_file
from src.reports import spending_by_category
from src.services import get_transactions_for_investment, investment_bank
from src.views import events


def main_events() -> list[dict]:
    """ Запускает работу приложения "События" для анализа транзакций """

    print("Здравствуйте!\nДобро пожаловать в приложение для анализа транзакций."
          "\nВведите дату, до которой будут рассматриваться транзакции. "
          "\nФормат даты должен быть следующим: \nДень.Месяц.Год Часы:Минуты:Секунды'\n")
    date = input()

    print("Выберите диапазон данных:\n"
          "W - неделя, на которую приходится дата;\n "
          "M -  месяц, на который приходится дата;\n"
          "Y - год, на который приходится дата;\n "
          "ALL - все данные до указанной даты за 3 последних месяца\n")

    date_range = input()
    if date_range not in ["W", "M", "Y", "ALL"]:
        date_range = "M"
    print(f"Выбран параметр {date_range} для временного диапазона")

    return events(date, date_range)


def main_investment() -> float:
    """ Запускает работу приложения "Инвесткопилка" для анализа транзакций """

    print("Запустить приложение 'Инвесткопилка'? Да/Нет")
    user_answer = input()
    if user_answer.lower() != "да":
        print("Приложение 'Инвесткопилка' не запускалось")
        return 0
    transactions = get_transactions_for_investment()

    month = input("Введите месяц, для которого рассчитывается отложенная сумма."
                  "Строка должна быть в формате 'YYYY-MM'")
    try:
        limit = int(input("Введите предел, до которого нужно округлять суммы операций (10 Р/ 50 Р/ 100 Р"))
    except Exception as error_text:
        print("Неправильный формат параметра 'предел'")

    return investment_bank(month, transactions, limit)

def main_spending_by_category() -> list[dict]:
    """ Запускает работу приложения "Траты по категории" для анализа транзакций """

    print("Запустить приложение 'Траты по категории'? Да/Нет")
    user_answer = input()
    if user_answer.lower() != "да":
        print("Приложение 'Траты по категории' не запускалось")
        return [{}]

    category_name = input("Ведите название категории")
    date = input("\nВведите дату, до которой будут рассматриваться транзакции. "
          "\nФормат даты должен быть следующим: \nДень.Месяц.Год Часы:Минуты:Секунды'\n")
    transactions = read_excel_file(PATH_TO_EXCEL_FILE)

    
    return spending_by_category(transactions, category_name, date)


def main_interface() -> None:
    """ Запускает общее приложение """
    json_events = main_events()
    float_investment = main_investment()
    json_spending_by_category = main_spending_by_category()

    print(
        f"Результаты работы основного приложения: "
        f"\nРезультат работы приложения 'События':  {json_events} "
        f"\nРезультат работы приложения 'Инвесткопилка':  {float_investment}"
        f"\nРезультат работы приложения 'Траты по категории':  {json_spending_by_category}"
    )


if __name__ == "__main__":

    json_events = main_events()
    float_investment = main_investment()
    json_spending_by_category = main_spending_by_category()

    print(
        f"Результаты работы основного приложения: "
        f"\nРезультат работы приложения 'События':  {json_events} "
        f"\nРезультат работы приложения 'Инвесткопилка':  {float_investment}"
        f"\nРезультат работы приложения 'Траты по категории':  {json_spending_by_category}"
          )
