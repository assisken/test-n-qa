from contextlib import nullcontext

import pytest
from pytest_mock import MockerFixture

from perf_calculator import (
    validate_salary,
    calculate_level_bonus,
    validate_perf_level,
    calculate_perf_bonus,
    calculate_salary_bonus,
)


@pytest.mark.parametrize(
    "salary, expectation",
    [
        (69999, pytest.raises(ValueError, match="Is too small")),
        (70000, nullcontext()),
        (750000, nullcontext()),
        (750001, pytest.raises(ValueError, match="Is too big")),
        (
            "foo",
            pytest.raises(
                AssertionError, match="Incorrect type for value. Expected int, got"
            ),
        ),
        (
            0.0,
            pytest.raises(
                AssertionError, match="Incorrect type for value. Expected int, got"
            ),
        ),
    ],
)
def test_validate_salary(salary, expectation):
    with expectation:
        validate_salary(salary)


@pytest.mark.parametrize(
    "level, expectation",
    [
        (6, pytest.raises(ValueError, match="Is too small")),
        (7, nullcontext()),
        (15, nullcontext()),
        (16, pytest.raises(ValueError, match="Is too big")),
        (
            "foo",
            pytest.raises(
                AssertionError, match="Incorrect type for value. Expected int, got"
            ),
        ),
        (
            0.0,
            pytest.raises(
                AssertionError, match="Incorrect type for value. Expected int, got"
            ),
        ),
    ],
)
def test_validate_salary(level, expectation):
    with expectation:
        calculate_level_bonus(level)


@pytest.mark.parametrize(
    "perf_level, expectation",
    [
        (0.0, pytest.raises(ValueError, match="Is too small")),
        (1.0, nullcontext()),
        (5.0, nullcontext()),
        (6.0, pytest.raises(ValueError, match="Is too big")),
        (
            "foo",
            pytest.raises(
                AssertionError, match="Incorrect type for value. Expected .*, got .*"
            ),
        ),
        (
            1,
            pytest.raises(
                AssertionError, match="Incorrect type for value. Expected .*, got .*"
            ),
        ),
    ],
)
def test_validate_salary(perf_level, expectation):
    with expectation:
        validate_perf_level(perf_level)


@pytest.mark.parametrize(
    "given, expected",
    [
        (9, 0.05),
        (10, 0.1),
        (12, 0.1),
        (13, 0.15),
        (14, 0.15),
        (15, 0.2),
    ],
)
def test_calculate_level_bonus(given, expected, mocker: MockerFixture):
    mocked_validator = mocker.patch("perf_calculator.validate_level")

    assert calculate_level_bonus(given) == expected
    mocked_validator.assert_called_once()


@pytest.mark.parametrize(
    "given, expected",
    [
        (1.0, 0.25),
        (2.4, 0.25),
        (2.5, 0.5),
        (2.9, 0.5),
        (3.0, 1),
        (3.4, 1),
        (3.5, 1.5),
        (3.9, 1.5),
        (4, 2),
    ],
)
def test_calculate_perf_level_bonus(given, expected, mocker: MockerFixture):
    mocked_validator = mocker.patch("perf_calculator.validate_perf_level")

    assert calculate_perf_bonus(given) == expected
    mocked_validator.assert_called_once()


@pytest.mark.parametrize(
    "salary, level, perf_level, expected",
    [
        # Result of AllPairs([
        #     (75_000, 100_000),
        #     (9, 11, 14, 15),
        #     (2.0, 2.7, 3.3, 3.7, 4.3),
        # ])
        (75000, 9, 2.0, 937.5),
        (75000, 15, 2.7, 7500.0),
        (75000, 14, 3.3, 11250.0),
        (75000, 11, 3.7, 11250.0),
        (75000, 11, 4.3, 15000.0),
        (100000, 11, 2.0, 2500.0),
        (100000, 14, 2.7, 7500.0),
        (100000, 15, 3.3, 20000.0),
        (100000, 9, 3.7, 7500.0),
        (100000, 9, 4.3, 10000.0),
        (100000, 14, 4.3, 30000.0),
        (100000, 14, 3.7, 22500.0),
        (100000, 15, 3.7, 30000.0),
        (100000, 9, 3.3, 5000.0),
        (100000, 11, 3.3, 10000.0),
        (100000, 11, 2.7, 5000.0),
        (100000, 9, 2.7, 2500.0),
        (100000, 15, 2.0, 5000.0),
        (100000, 14, 2.0, 3750.0),
    ],
)
def test_calculate_salary_bonus(salary, level, perf_level, expected):
    assert calculate_salary_bonus(salary, level, perf_level) == expected
