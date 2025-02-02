import os

import requests
from dotenv import load_dotenv

from src.utils import BASE_DIR
from tests.conftest import data_for_test_get_get_currencies_rate

# Задаю путь к JSON-файлу с запросами валют и акций
PATH_TO_USER_SETTINGS_FILE = os.path.join(BASE_DIR, "user_settings.json")
# URL для сайта Exchange Rates Data API
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"
# URL для сайта Exchange Rates Data API
STOCK_URL = "https://www.alphavantage.co/query"


def get_currency_rate(currency: str) -> dict:
    """
    Принимает на вход уть к файлу с запросом валют и акций.
    Возвращает актуальный курс для запрошенных валют и акций
    """
    load_dotenv()
    apikey = os.getenv("API_KEY")
    headers = {"apikey": f"{apikey}"}
    params = {"to": "RUB", "from": currency, "amount": 1}
    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
    except requests.exceptions.RequestException:
        print("Ошибка при работе с HTTP запросом")
        return {}

    if response.status_code != 200:
        print(f"Получены неправильные данные от API. Status_code = {response.status_code}")
        return {}
    answer_api = response.json()
    try:
        currency_rate = answer_api["result"]
        # currency_rate = float("{:.2f}".format(answer_api["result"]))
    except Exception as error_text:
        print(f"\nНекорректные данные в ответе от API. Код ошибки: {error_text}")
        return {}
    currencies_rate_dict = {"currency": currency, "rate": currency_rate}

    return currencies_rate_dict


# def get_stocks_price(currencies_and_stocks: dict) -> list(dict):
#     """
#     Принимает на вход уть к файлу с запросом валют и акций.
#     Возвращает актуальный курс для запрошенных валют и акций
#     """
#     stocks_list = currencies_and_stocks["user_stocks"]
#     stocks_price = []
#     for stock in stocks_list:
#         # function=TIME_SERIES_DAILY&symbol=TSCO.LON&outputsize=full&apikey=demo
#         #https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo
#         # https: // www.alphavantage.co / query?function = TIME_SERIES_DAILY & symbol = TSCO.LON &
#         # outputsize = full & apikey = demo
#         # https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=IBM&apikey=demo
#         # https://cloud.iexapis.com/stable/stock/{symbol}/quote
#
#         load_dotenv()
#         apikey = os.getenv("API_KEY_ALPHA_VANTAGE")
#         # apikey = os.getenv("API_KEY")
#         headers = {"apikey": f"{apikey}"}
#         params = {"function": "TIME_SERIES_WEEKLY", "symbol": stock}
#         try:
#             response = requests.get(STOCK_URL, headers=headers, params=params)
#
#         except requests.exceptions.RequestException:
#             print("Ошибка при работе с HTTP запросом")
#             return None
#
#         if response.status_code != 200:
#             print(f"Получены неправильные данные от API. Status_code = {response.status_code}")
#             return None
#         answer_api = response.json()
#         try:
#             # stock_price = answer_api
#             stock_price = answer_api["Weekly Time Series"]["2025-01-31"]["4. close"]
#         except Exception as error_text:
#             print(f"\nНекорректные данные в ответе от API. Код ошибки: {error_text}")
#             return None
#         stocks_price.append((stock, round(float(stock_price), 2)))
#
#     stocks_price_list = [{"stock": stock, "price": price}
#                                 for stock, price in stocks_price]
#
#
#     return stocks_price_list


if __name__ == "__main__":
    print(get_currency_rate("USD"))
