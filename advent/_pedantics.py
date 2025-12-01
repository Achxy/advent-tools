"""
MIT License

Copyright (c) 2022-present Achyuth Jayadevan <achyuth@jayadevan.in>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from functools import partial
from typing import Any, TypeVar

from ._exceptions import DateValidationError

_T = TypeVar("_T")
_T2 = TypeVar("_T2")

START_OF_AOC_YEAR = 2015
UTC_5 = timezone(timedelta(hours=-5))
now = partial(datetime.now, tz=UTC_5)


@dataclass(frozen=True, slots=True)
class YearDayRange:
    """Defines the maximum number of days for a range of AOC years.

    Attributes:
        start_year: First year this range applies to (inclusive).
        end_year: Last year this range applies to (inclusive), or None for unbounded.
        max_days: Maximum number of puzzle days available in this year range.
    """

    start_year: int
    end_year: int | None
    max_days: int

    def __post_init__(self) -> None:
        if self.end_year is not None and self.start_year > self.end_year:
            raise ValueError(f"start_year ({self.start_year}) cannot be greater than end_year ({self.end_year})")
        if self.max_days < 1:
            raise ValueError(f"max_days must be at least 1, got {self.max_days}")

    def contains_year(self, year: int) -> bool:
        """Check if the given year falls within this range."""
        if year < self.start_year:
            return False
        if self.end_year is None:
            return True
        return year <= self.end_year


AOC_DAY_RANGES: tuple[YearDayRange, ...] = (
    YearDayRange(start_year=2015, end_year=2024, max_days=25),
    YearDayRange(start_year=2025, end_year=None, max_days=12),
)


def get_max_days_for_year(year: int) -> int:
    """Get the maximum number of puzzle days for a given AOC year.

    Args:
        year: The AOC year to look up.

    Returns:
        The maximum number of days available for that year.

    Raises:
        ValueError: If no range is defined for the given year.
    """
    for year_range in AOC_DAY_RANGES:
        if year_range.contains_year(year):
            return year_range.max_days
    raise ValueError(f"No day range defined for year {year}")


def not_both_provided_but_one(a: _T | None, b: _T2 | None, msg: str = "Provide exactly one value") -> _T | _T2:
    if (a is None) is (b is None):
        raise ValueError(msg)
    return a if a is not None else b  # type: ignore[return-value]


def check_type(varname: str, value: Any, expected: type[_T], *, strict: bool = False) -> _T:
    if not isinstance(value, expected):
        raise TypeError(f"{varname!r} must be of type {expected.__name__!r}, not {type(value).__name__!r}")
    if strict and type(value) is not expected:
        raise TypeError(f"{varname!r} must be strictly type {expected.__name__!r}, not {type(value).__name__!r}")
    return value


def check_if_can_be_well_formatted(unformatted: str, *args: str) -> None:
    """Validate that a format string contains the required placeholders."""
    check_type("unformatted", unformatted, str, strict=True)
    try:
        unformatted.format(**dict.fromkeys(args, ""))
    except KeyError as exc:
        raise ValueError(f"Unformatted string has missing keys (string: {unformatted!r})") from exc
    except IndexError as exc:
        raise ValueError(f"No index-based formatting allowed for this context (string: {unformatted!r})") from exc


def check_if_valid_year(year: int) -> int:
    """Validate that a year is within the valid AOC range."""
    check_type("year", year, int)
    current_year = now().year
    if year < START_OF_AOC_YEAR:
        raise DateValidationError(f"Year {year} is before the start of Advent of Code ({START_OF_AOC_YEAR})")
    if year > current_year:
        raise DateValidationError(f"Year {year} is in the future (current year: {current_year})")
    return year


def check_if_valid_day(day: int, *, year: int) -> int:
    """Validate that a day is within the valid AOC range for a given year.

    Args:
        day: The day number to validate.
        year: The year to determine the max days allowed.

    Returns:
        The validated day number.

    Raises:
        DateValidationError: If the day is out of range.
        TypeError: If day is not an integer.
    """
    check_type("day", day, int)
    if day < 1:
        raise DateValidationError(f"Day {day} is less than 1")

    max_days = get_max_days_for_year(year)
    if day > max_days:
        raise DateValidationError(f"Day {day} exceeds maximum AOC days ({max_days})")
    return day


def check_if_viable_date(year: int, day: int) -> None:
    """Validate that a year/day combination is available for fetching."""
    check_if_valid_year(year)
    check_if_valid_day(day, year=year)

    current_time = now()
    current_year = current_time.year
    is_december = current_time.month == 12

    # Past years are always available
    if year < current_year:
        return

    # Current year but not December yet
    if not is_december:
        months_to_wait = 12 - current_time.month
        raise DateValidationError(f"Advent of Code only runs in December. Wait {months_to_wait} more month(s).")

    # Check if the specific day is available
    puzzle_release = datetime(year, 12, day, tzinfo=UTC_5)
    if current_time < puzzle_release:
        delta = puzzle_release - current_time
        total_seconds = int(delta.total_seconds())
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        raise DateValidationError(f"Day {day} puzzle not yet released. Time remaining: {days}d {hours}h {minutes}m {seconds}s")
