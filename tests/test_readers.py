import os
from typing import Any
from unittest.mock import patch, mock_open
import pandas as pd

from src.readers import read_excel_file, read_json_file
from src.utils import PATH_TO_USER_SETTINGS_FILE
from src.writer import writing_dataframe_to_dict


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
    assert read_excel_file(PATH_TO_USER_SETTINGS_FILE) == []

def test_read_json_file() -> None:
    """Проверяет работу функции read_json_file"""
    # Функция с данными data_for_read_json_file находится в файле operations_for_tests.py
    assert read_json_file(PATH_TO_USER_SETTINGS_FILE) == {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN"]
    }

def test_read_json_file_wrong_path() -> None:
    """
    Проверяет, что функция read_json_file выдаёт пустой список,
    если JSON-файл со списком не найден
    """
    path_to_file = os.path.join(os.path.dirname(__file__), "operations.json")
    assert read_json_file(path_to_file) == {}

def test_read_json_file_empty() -> None:
    """
    Проверяет, что функция read_json_file выдаёт пустой список,
    если JSON-файл содержит пустой список
    """
    mocked_open = mock_open(read_data="[]")
    with patch("builtins.open", mocked_open):
        result = read_json_file(PATH_TO_USER_SETTINGS_FILE)
    assert result == {}
    mocked_open.assert_called_once_with(PATH_TO_USER_SETTINGS_FILE)

def test_read_json_file_not_list() -> None:
    """
    Проверяет, что функция read_json_file выдаёт пустой список,
    если JSON-файл содержит не словарь
    """
    mocked_open = mock_open(read_data="key: Value")
    with patch("builtins.open", mocked_open):
        result = read_json_file(PATH_TO_USER_SETTINGS_FILE)
    assert result == {}
    mocked_open.assert_called_once_with(PATH_TO_USER_SETTINGS_FILE)

def test_read_json_file_json_decode_error() -> None:
    """
    Проверяет работу функции read_json_file
    при ошибке декодирования JSON-файла
    """
    mocked_open = mock_open(read_data='{"key: "Value"}')
    with patch("builtins.open", mocked_open):
        result = read_json_file(PATH_TO_USER_SETTINGS_FILE)
    assert result == {}
    mocked_open.assert_called_once_with(PATH_TO_USER_SETTINGS_FILE)
