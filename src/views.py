import datetime

from src.utils import get_json_answer


def events(date: str, date_range: str= "M") -> list[dict]:
    """
    Принимает на вход строку с датой и второй необязательный параметр — диапазон данных. По умолчанию диапазон равен
    одному месяцу (с начала месяца, на который выпадает дата, по саму дату). Возможные значения второго
    необязательного параметра:
    W — неделя, на которую приходится дата;
    M — месяц, на который приходится дата;
    Y — год, на который приходится дата;
    ALL — все данные за последние 3 месяца до указанной даты.
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

    json_answer = get_json_answer(date, date_range)

    return  json_answer
