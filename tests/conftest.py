import os

from dotenv import load_dotenv


def data_for_test_get_get_currencies_rate() -> dict:
    """ Возвращает данные из файла user_settings.json"""
    load_dotenv()
    apikey = os.getenv("API_KEY")
    headers = {"apikey": f"{apikey}"}
    params = {"to": "RUB", "from": ["USD", "EUR"], "amount": 1}
    currencies_and_stocks = {
  "user_currencies": ["USD", "EUR"],
  "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
        }
    return currencies_and_stocks, headers, params