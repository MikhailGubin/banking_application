import json

from src.utils import get_json_answer


def events(date: str, date_range: str = "M") -> str | list[dict]:
    """
    Принимает на вход строку с датой и второй необязательный параметр — диапазон данных. По умолчанию диапазон равен
    одному месяцу (с начала месяца, на который выпадает дата, по саму дату).
    Возвращаемый JSON-ответ содержит следующие данные:
    «Расходы», «Поступления», курс валют, стоимость акций из S&P 500
    """

    json_answer = get_json_answer(date, date_range)

    if json_answer == [{}]:
        return json.dumps([{}])

    return json_answer
