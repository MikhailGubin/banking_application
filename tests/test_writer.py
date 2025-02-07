import pandas as pd
import pytest

from src.writer import writing_dataframe_to_dict


def test_writing_dataframe_to_dict() -> None:
    """
    Проверяет работу функции writing_dataframe_to_dict
    """

    df_excel_file = pd.DataFrame(
        {
            "Дата операции": ["01.01.2018 20:27:51", "01.01.2018 12:49:53", "03.11.2021 15:03:35"],
            "Категория": ["Красота", "Переводы", "Супермаркеты"],
            "Сумма платежа": [-316.0, -3000.0, -73.06],
        }
    )
    assert writing_dataframe_to_dict(df_excel_file) == [
        {"Дата операции": "01.01.2018 20:27:51", "Категория": "Красота", "Сумма платежа": -316.0},
        {"Дата операции": "01.01.2018 12:49:53", "Категория": "Переводы", "Сумма платежа": -3000.0},
        {"Дата операции": "03.11.2021 15:03:35", "Категория": "Супермаркеты", "Сумма платежа": -73.06},
    ]


@pytest.mark.parametrize(
    "wrong_data_in_file", [({"Yes": [50, 131, 12], "No": [21, 2]}), ({"Yes", "No"}), (pd.DataFrame({}))]
)
def test_writing_dataframe_to_dict_wrong_data(wrong_data_in_file: any) -> None:
    """
    Проверяет работу функции writing_dataframe_to_dict,
    когда файл содержит неверные данные
    """

    assert writing_dataframe_to_dict(wrong_data_in_file) == [{}]
