"""Tests for the _pedantics module."""

import pytest

from advent._exceptions import DateValidationError
from advent._pedantics import (
    MAX_AOC_DAYS,
    START_OF_AOC_YEAR,
    check_if_can_be_well_formatted,
    check_if_valid_day,
    check_if_valid_year,
    check_type,
    not_both_provided_but_one,
)


class TestCheckType:
    def test_accepts_valid_type(self) -> None:
        assert check_type("x", 42, int) == 42
        assert check_type("x", "hello", str) == "hello"
        assert check_type("x", [1, 2, 3], list) == [1, 2, 3]

    def test_accepts_subclass(self) -> None:
        class MyInt(int):
            pass

        assert check_type("x", MyInt(5), int) == 5

    def test_rejects_invalid_type(self) -> None:
        with pytest.raises(TypeError, match="must be of type"):
            check_type("x", "hello", int)

    def test_strict_mode_rejects_subclass(self) -> None:
        class MyInt(int):
            pass

        with pytest.raises(TypeError, match="strictly type"):
            check_type("x", MyInt(5), int, strict=True)


class TestNotBothProvidedButOne:
    def test_returns_first_when_second_is_none(self) -> None:
        assert not_both_provided_but_one(42, None) == 42

    def test_returns_second_when_first_is_none(self) -> None:
        assert not_both_provided_but_one(None, 42) == 42

    def test_raises_when_both_none(self) -> None:
        with pytest.raises(ValueError):
            not_both_provided_but_one(None, None)

    def test_raises_when_both_provided(self) -> None:
        with pytest.raises(ValueError):
            not_both_provided_but_one(1, 2)

    def test_custom_message(self) -> None:
        with pytest.raises(ValueError, match="custom"):
            not_both_provided_but_one(None, None, "custom message")


class TestCheckIfCanBeWellFormatted:
    def test_valid_format_string(self) -> None:
        check_if_can_be_well_formatted("{year}/{day}", "year", "day")

    def test_missing_key_raises(self) -> None:
        with pytest.raises(ValueError, match="missing keys"):
            check_if_can_be_well_formatted("{year}/{month}", "year", "day")

    def test_index_based_raises(self) -> None:
        with pytest.raises(ValueError, match="index-based"):
            check_if_can_be_well_formatted("{0}/{1}", "year", "day")

    def test_rejects_non_string(self) -> None:
        with pytest.raises(TypeError):
            check_if_can_be_well_formatted(123, "year", "day")  # type: ignore[arg-type]


class TestCheckIfValidYear:
    def test_accepts_valid_years(self) -> None:
        for year in range(START_OF_AOC_YEAR, 2025):
            assert check_if_valid_year(year) == year

    def test_rejects_pre_aoc_year(self) -> None:
        with pytest.raises(DateValidationError, match="before the start"):
            check_if_valid_year(2014)

    def test_rejects_far_future(self) -> None:
        with pytest.raises(DateValidationError, match="future"):
            check_if_valid_year(3000)

    def test_rejects_non_int(self) -> None:
        with pytest.raises(TypeError):
            check_if_valid_year("2022")  # type: ignore[arg-type]


class TestCheckIfValidDay:
    def test_accepts_valid_days(self) -> None:
        for day in range(1, MAX_AOC_DAYS + 1):
            assert check_if_valid_day(day) == day

    def test_rejects_day_zero(self) -> None:
        with pytest.raises(DateValidationError, match="less than 1"):
            check_if_valid_day(0)

    def test_rejects_negative_day(self) -> None:
        with pytest.raises(DateValidationError, match="less than 1"):
            check_if_valid_day(-1)

    def test_rejects_day_over_25(self) -> None:
        with pytest.raises(DateValidationError, match="exceeds maximum"):
            check_if_valid_day(26)

    def test_rejects_non_int(self) -> None:
        with pytest.raises(TypeError):
            check_if_valid_day("5")  # type: ignore[arg-type]
