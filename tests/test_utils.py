import datetime
from typing import Any
import pandas as pd
import pytest
from src.utils import writing_dataframe_to_dict, get_date_range



@pytest.mark.parametrize(
    "wrong_data_in_file", [({"Yes": [50, 131, 12], "No": [21, 2]}), ({"Yes", "No"}), (pd.DataFrame({}))]
)
def test_writing_dataframe_to_dict(wrong_data_in_file: Any) -> None:
    """
    Проверяет работу функции read_excel_file,
    когда файл содержит неверные данные    """

    assert writing_dataframe_to_dict(wrong_data_in_file) == [{}]


@pytest.mark.parametrize(
    "date, date_range, expected", [
    ("25.11.2021 14:33:34", "M",
     (datetime.datetime(2021, 11, 1, 0, 0),
     datetime.datetime(2021, 11, 25, 14, 33, 34))
     ),
    ("25.11.2021 14:33:34", "ALL",
     (datetime.datetime(2021, 8, 1, 0, 0),
     datetime.datetime(2021, 11, 25, 14, 33, 34))
     ),
        ("25.01.2021 14:33:34", "ALL",
         (datetime.datetime(2020, 10, 1, 0, 0),
          datetime.datetime(2021, 1, 25, 14, 33, 34))
         ),
    ("1.1.2022 14:33:34", "W",
     (datetime.datetime(2021, 12, 27, 0, 0),
     datetime.datetime(2022, 1, 1, 14, 33, 34))
     ),
    ("25.11.2021 14:33:34", "Y",
     (datetime.datetime(2021, 1, 1, 0, 0),
     datetime.datetime(2021, 11, 25, 14, 33, 34))
     )
    ]
)
def test_get_date_range(date: str, date_range: str, expected: tuple) -> None:
    """ Проверяет работу функции get_date_range"""

    assert get_date_range(date, date_range) == expected

@pytest.mark.parametrize(
    "date, date_range", [
    (123, "M"),
    ("string", "ALL"),
    ("25.01.2021 14:33:34", "A")
        ]
    )
def test_get_date_range_wrong_date(date: str, date_range: str) -> None:
    """
    Проверяет работу функции get_date_range,
    сли на вход передана неправильная дата
    """

    assert get_date_range(date, date_range) is None
