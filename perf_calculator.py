from functools import partial
from typing import Type, TypeVar

T = TypeVar("T")


def _validate(value: int, _type: Type[T], min_value: T, max_value: T):
    assert isinstance(
        value, _type
    ), f"Incorrect type for value. Expected {_type}, got {type(value)}"

    if value < min_value:
        raise ValueError("Is too small")
    if value > max_value:
        raise ValueError("Is too big")


validate_salary = partial(_validate, _type=int, min_value=70_000, max_value=750_000)
validate_level = partial(_validate, _type=int, min_value=7, max_value=15)
validate_perf_level = partial(_validate, _type=float, min_value=1, max_value=5)


def calculate_level_bonus(level: int) -> float:
    validate_level(level)

    if level < 10:
        return 0.05
    elif 10 <= level < 13:
        return 0.1
    elif 13 <= level < 15:
        return 0.15
    else:
        return 0.2


def calculate_perf_bonus(perf_level: float) -> float:
    validate_perf_level(perf_level)

    if 1 <= perf_level < 2.5:
        return 0.25
    elif 2.5 <= perf_level < 3:
        return 0.5
    elif 3 <= perf_level < 3.5:
        return 1
    elif 3.5 <= perf_level < 4:
        return 1.5
    else:
        return 2


def calculate_salary_bonus(salary: int, level: int, perf_level: float) -> float:
    validate_salary(salary)

    return salary * calculate_level_bonus(level) * calculate_perf_bonus(perf_level)
