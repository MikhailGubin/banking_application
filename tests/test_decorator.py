import os
from typing import Any

from freezegun import freeze_time

from src.decorator import log, summ_two_numbers

PATH_TO_TXT_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "function_log.txt")


def test_summ_two_numbers() -> None:
    """
    Проверяет работу декоратора log
    """

    result = summ_two_numbers(1, 2)
    assert result == 3


@freeze_time("2023-01-01")
def test_log_read_in_file() -> None:
    """
    Проверяет вывод сообщений декоратором log в файл

    """
    summ_two_numbers(4, 1)
    with open(PATH_TO_TXT_FILE, "r", encoding="utf-8") as file:
        content = file.read().split("\n")
    assert content[-3:-1] == [
        "summ_two_numbers ok, result: 5",
        "start - 2023-01-01 00:00:00; stop - 2023-01-01 00:00:00",
    ]


@freeze_time("2023-01-01")
def test_log_typeerror() -> None:
    """
    Проверяет, что декоратор loq корректно
    обрабатывает входные аргументы неправильного типа данных
    """
    summ_two_numbers(1, "2")
    with open(PATH_TO_TXT_FILE, "r", encoding="utf-8") as file:
        content = file.read().split("\n")
    assert content[-3:-1] == [
        "summ_two_numbers error: unsupported operand type(s) for +: 'int' and 'str'. " "Inputs: (1, '2'), {}",
        "start - 2023-01-01 00:00:00; stop - 2023-01-01 00:00:00",
    ]


@freeze_time("2023-01-01")
def test_log_error() -> None:
    """
    Проверяет, что декоратор loq корректно
    отрабатывает отсутствие нужного количества входных аргументов
    """
    summ_two_numbers(
        1,
    )
    with open(PATH_TO_TXT_FILE, "r", encoding="utf-8") as file:
        content = file.read().split("\n")
    assert content[-3:-1] == [
        "summ_two_numbers error: summ_two_numbers() missing 1 required positional argument: 'y'. " "Inputs: (1,), {}",
        "start - 2023-01-01 00:00:00; stop - 2023-01-01 00:00:00",
    ]


@freeze_time("2023-01-01")
def test_log_message(capsys: Any) -> None:
    """
    Проверяет вывод сообщений декоратора log в консоль
    """

    @log(filename=None)
    def summ_numbers(x: int | float, y: int | float) -> int | float:
        """
        Складывает два числа
        """
        return x + y

    summ_numbers(1, 2)
    captured = capsys.readouterr()
    assert captured.out == "summ_numbers ok, result: 3\nstart - 2023-01-01 00:00:00; stop - 2023-01-01 00:00:00\n"
