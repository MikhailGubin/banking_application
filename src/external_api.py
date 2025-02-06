import os

import requests
from dotenv import load_dotenv


# URL для сайта Exchange Rates Data API
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"
# URL для сайта Exchange Rates Data API
STOCK_URL = "https://api.twelvedata.com/time_series"


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
        currency_rate = float("{:.2f}".format(answer_api["result"]))
    except Exception as error_text:
        print(f"\nНекорректные данные в ответе от API. Код ошибки: {error_text}")
        return {}
    currencies_rate_dict = {"currency": currency, "rate": currency_rate}

    return currencies_rate_dict


def get_stocks_price(stock: str) -> dict:
    """
    Принимает на вход уть к файлу с запросом валют и акций.
    Возвращает актуальный курс для запрошенных валют и акций
    """

    load_dotenv()
    apikey_stock = os.getenv("API_KEY_TWELVE_DATA")

    try:
        response = requests.get(f"https://api.twelvedata.com/time_series?symbol={stock}&interval=1h&"
                                f"apikey={apikey_stock}")
    except requests.exceptions.RequestException:
        print("Ошибка при работе с HTTP запросом")
        return {}

    if response.status_code != 200:
        print(f"Получены неправильные данные от API. Status_code = {response.status_code}")
        return {}
    answer_api = response.json()
    try:
        # stock_price = answer_api
        stock_price = float(answer_api['values'][0]['close'])
    except Exception as error_text:
        print(f"\nНекорректные данные в ответе от API. Код ошибки: {error_text}")
        return {}

    stock_price_dict = {"stock": stock, "price": round(stock_price, 2)}

    return stock_price_dict
