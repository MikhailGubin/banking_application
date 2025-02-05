import datetime
import os
from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Логирует начало и конец выполнения функции, а также ее результаты
    или возникшие ошибки
    """

    def decorator(func: Any) -> Any:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                error_text = ""
                # объявляю переменную под запись ошибок
                time_start = datetime.datetime.now()
                result = func(*args, **kwargs)

            except Exception as error_message:
                error_text = str(error_message)

            else:

                time_stop = datetime.datetime.now()
                message = f"{func.__name__} ok, result: {result}\nstart - {time_start}; stop - {time_stop}"

            finally:

                if error_text:
                    time_stop = datetime.datetime.now()
                    message = (
                        f"{func.__name__} error: {error_text}. Inputs: {args}, {kwargs}\n"
                        f"start - {time_start}; stop - {time_stop}"
                    )
                    result = None

                if filename:

                    path = os.path.join(os.path.dirname(__file__), "..", "data", f"{filename}.txt")
                    with open(path, "a", encoding="utf-8") as file:
                        file.write(message + "\n")
                else:
                    print(message)

                return result

        return wrapper

    return decorator


@log(filename="function_log")
def summ_two_numbers(x: int | float, y: int | float) -> int | float:
    """
    Складывает два числа
    """
    return x + y
