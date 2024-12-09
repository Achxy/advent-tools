from datetime import datetime, timedelta, timezone
from functools import partial
from typing import Any, TypeVar

_T = TypeVar("_T")
_T2 = TypeVar("_T2")

START_OF_AOC_YEAR = 2015
MAX_AOC_DAYS = 25
UTC_5 = timezone(timedelta(hours=-5))
now = partial(datetime.now, tz=UTC_5)


def not_both_provided_but_one(a: _T | None, b: _T2 | None, msg: str = "Provide exactly one value") -> _T | _T2:
    if (a is None) is (b is None):
        raise ValueError(msg)
    return a if a is not None else b  # type: ignore (typecheckers don't understand this)


def check_type(varname: str, value: Any, expected: type[_T], strict: bool = False) -> _T:
    if not isinstance(value, expected):
        raise TypeError(f"{varname} must be of type {expected!r} or it's subclasses, not {type(value)!r}")
    if strict and type(value) is not expected:
        raise TypeError(f"{varname} must be of strictly type {expected!r}, not {type(value)!r}")
    return value


def check_if_can_be_well_formatted(unformatted: str, *args: str):
    # Make sure side-effectless
    check_type("unformatted", unformatted, str, strict=True)
    try:
        unformatted.format(**{i: str() for i in args})
    except KeyError as exc:
        raise ValueError(f"Unformatted string has missing keys (string: {unformatted})") from exc
    except IndexError as exc:
        raise ValueError(f"No index-based formatting allowed for this context (string: {unformatted})") from exc


def check_if_valid_year(year: int) -> int:
    check_type("year", year, int)
    current_year = now().year
    if year < START_OF_AOC_YEAR:
        raise ValueError(f"Current year is {current_year}, which is before the start of Advent of Code: {START_OF_AOC_YEAR}")
    if year > now().year:
        raise ValueError(f"{year} is in the future, current year is {current_year}")
    return year


def check_if_valid_day(day: int) -> int:
    check_type("day", day, int)
    if day > MAX_AOC_DAYS:
        raise ValueError(f"Day {day} is greater than the maximum number of days in Advent of Code: {MAX_AOC_DAYS}")
    if day < 1:
        raise ValueError(f"Day {day} is less than 1")
    return day


def check_if_viable_date(year: int, day: int):
    check_if_valid_day(day)
    check_if_valid_year(year)
    current_year, current_day = now().year, now().day
    is_december = now().month == 12
    if year < current_year:
        return
    if not is_december:
        delta = 12 - now().month
        raise ValueError(f"Advent of Code only happens in December, you'll have to wait {delta} more months")
    if day > current_day + 1:
        raise ValueError(f"Day {day} is in the future, current available day is {current_day}")
    if not now() >= datetime(year, 12, day, tzinfo=UTC_5):
        delta = datetime(year, 12, day, tzinfo=UTC_5) - now()
        fmt = f"{delta.seconds // 3600} hours, {(delta.seconds // 60) % 60} minutes and {delta.seconds % 60} seconds"
        raise ValueError(f"Advent of Code for day {day} has not started yet ({fmt} left)")
