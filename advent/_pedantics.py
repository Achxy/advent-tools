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

from datetime import datetime, timedelta, timezone
from functools import partial
from typing import Any, TypeVar

from ._exceptions import DateValidationError

_T = TypeVar("_T")
_T2 = TypeVar("_T2")

START_OF_AOC_YEAR = 2015
MAX_AOC_DAYS = 25
UTC_5 = timezone(timedelta(hours=-5))
now = partial(datetime.now, tz=UTC_5)


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


def check_if_valid_day(day: int) -> int:
    """Validate that a day is within the valid AOC range (1-25)."""
    check_type("day", day, int)
    if day > MAX_AOC_DAYS:
        raise DateValidationError(f"Day {day} exceeds maximum AOC days ({MAX_AOC_DAYS})")
    if day < 1:
        raise DateValidationError(f"Day {day} is less than 1")
    return day


def check_if_viable_date(year: int, day: int) -> None:
    """Validate that a year/day combination is available for fetching."""
    check_if_valid_day(day)
    check_if_valid_year(year)

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
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        raise DateValidationError(f"Day {day} puzzle not yet released. Time remaining: {hours}h {minutes}m {seconds}s")
