import json
import os
from typing import Any
from unittest.mock import patch

import pandas as pd
import pytest

from src.utils import read_excel_file, writing_dataframe_to_dict, user_request


# from src.utils import LOG_PATH


@patch("pandas.read_excel")
def test_read_excel_file(mock_read: Any) -> None:
    """Проверяет работу функции read_excel_file"""
    mock_read.return_value = pd.DataFrame({"Yes": [50, 131], "No": [21, 2]})
    assert writing_dataframe_to_dict(read_excel_file("test.xlsx")) == [{'No': 21, 'Yes': 50}, {'No': 2, 'Yes': 131}]
    mock_read.assert_called_once_with("test.xlsx")


def test_read_excel_file_not_found() -> None:
    """
    Проверяет работу функции read_excel_file,
    когда Excel-файл не найден
    """
    assert read_excel_file("test.xlsx") == []


def test_read_excel_file_wrong_format() -> None:
    """
    Проверяет работу функции read_excel_file,
    когда на вход подаётся файл другого формата
    """
    # Получаю абсолютный путь к корневой директории проекта
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Задаю путь к CSV-файлу с транзакциями
    PATH_TO_README = os.path.join(BASE_DIR, "README.MD")
    assert read_excel_file(PATH_TO_README) == []


@pytest.mark.parametrize(
    "wrong_data_in_file", [({"Yes": [50, 131, 12], "No": [21, 2]}), ({"Yes", "No"}), (pd.DataFrame({}))]
)

def test_writing_dataframe_to_dict(wrong_data_in_file: Any) -> None:
    """
    Проверяет работу функции read_excel_file,
    когда файл содержит неверные данные    """

    assert writing_dataframe_to_dict(wrong_data_in_file) == [{}]


@patch("builtins.input", side_effect=["USD EUR", "AAPL AMZN GOOGL MSFT TSLA"])
def test_user_request(mock_input) -> None:
    """ Проверяет работу функции user_request"""

    assert user_request() == json.loads('{"user_currencies": ["USD", "EUR"], '
                                        '"user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}')
