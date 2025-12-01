"""Tests for the _pedantics module."""

import pytest

from advent._exceptions import DateValidationError
from advent._pedantics import (
    AOC_DAY_RANGES,
    START_OF_AOC_YEAR,
    YearDayRange,
    check_if_can_be_well_formatted,
    check_if_valid_day,
    check_if_valid_year,
    check_type,
    get_max_days_for_year,
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


class TestYearDayRange:
    def test_contains_year_bounded(self) -> None:
        r = YearDayRange(start_year=2015, end_year=2024, max_days=25)
        assert r.contains_year(2015) is True
        assert r.contains_year(2020) is True
        assert r.contains_year(2024) is True
        assert r.contains_year(2014) is False
        assert r.contains_year(2025) is False

    def test_contains_year_unbounded(self) -> None:
        r = YearDayRange(start_year=2025, end_year=None, max_days=12)
        assert r.contains_year(2025) is True
        assert r.contains_year(3000) is True
        assert r.contains_year(2024) is False

    def test_rejects_invalid_range(self) -> None:
        with pytest.raises(ValueError, match="cannot be greater than"):
            YearDayRange(start_year=2025, end_year=2020, max_days=25)

    def test_rejects_invalid_max_days(self) -> None:
        with pytest.raises(ValueError, match="must be at least 1"):
            YearDayRange(start_year=2015, end_year=2024, max_days=0)


class TestGetMaxDaysForYear:
    def test_returns_25_for_2015_to_2024(self) -> None:
        for year in range(2015, 2025):
            assert get_max_days_for_year(year) == 25

    def test_returns_12_for_2025_onwards(self) -> None:
        for year in [2025, 2026, 2030, 2100]:
            assert get_max_days_for_year(year) == 12

    def test_raises_for_undefined_year(self) -> None:
        with pytest.raises(ValueError, match="No day range defined"):
            get_max_days_for_year(2014)


class TestAocDayRangesIntegrity:
    def test_ranges_cover_all_aoc_years(self) -> None:
        """Ensure ranges cover from START_OF_AOC_YEAR and have an unbounded end."""
        assert AOC_DAY_RANGES[0].start_year == START_OF_AOC_YEAR
        assert AOC_DAY_RANGES[-1].end_year is None

    def test_ranges_are_contiguous(self) -> None:
        """Ensure there are no gaps between ranges."""
        for i in range(len(AOC_DAY_RANGES) - 1):
            current = AOC_DAY_RANGES[i]
            next_range = AOC_DAY_RANGES[i + 1]
            assert current.end_year is not None
            assert current.end_year + 1 == next_range.start_year


class TestCheckIfValidDay:
    def test_accepts_valid_days_for_pre_2025_year(self) -> None:
        for day in range(1, 26):
            assert check_if_valid_day(day, year=2023) == day

    def test_accepts_valid_days_for_2025_onwards(self) -> None:
        for day in range(1, 13):
            assert check_if_valid_day(day, year=2025) == day

    def test_rejects_day_over_12_for_2025(self) -> None:
        with pytest.raises(DateValidationError, match="exceeds maximum"):
            check_if_valid_day(13, year=2025)

    def test_rejects_day_over_25_for_pre_2025(self) -> None:
        with pytest.raises(DateValidationError, match="exceeds maximum"):
            check_if_valid_day(26, year=2020)

    def test_rejects_day_zero(self) -> None:
        with pytest.raises(DateValidationError, match="less than 1"):
            check_if_valid_day(0, year=2020)

    def test_rejects_negative_day(self) -> None:
        with pytest.raises(DateValidationError, match="less than 1"):
            check_if_valid_day(-1, year=2020)

    def test_rejects_non_int(self) -> None:
        with pytest.raises(TypeError):
            check_if_valid_day("5", year=2020)  # type: ignore[arg-type]
