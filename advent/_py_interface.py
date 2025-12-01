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

from collections.abc import Callable
from typing import Any

from ._benchmark import benchmark_and_print
from ._data_handle import get, get_example_data, getch
from ._exceptions import DataNotFoundError
from ._pedantics import not_both_provided_but_one
from ._typeshack import FakeGenericForGetItemSupport, FakeType


class _InstantiatorFromSlice(type):
    """
    Metaclass enabling Advent[YEAR:DAY] syntax for date specification.

    This allows users to write `class Solution(Advent[2022:1])` as an
    alternative to `class Solution(Advent, year=2022, day=1)`.
    """

    __year__: int | None = None
    __day__: int | None = None

    def __getitem__(cls, date: slice) -> Callable[..., type]:
        if date.step is not None:
            raise ValueError(f"Use {cls.__name__}[YEAR:DAY] syntax, not {cls.__name__}[YEAR:DAY:STEP]")
        cls.__year__ = date.start
        cls.__day__ = date.stop
        return cls


class Advent(FakeGenericForGetItemSupport[FakeType], metaclass=_InstantiatorFromSlice):
    """
    Base class for Advent of Code solutions.

    Usage:
        class Solution(Advent, year=2022, day=1):
            def __init__(self, data: str) -> None:
                self.data = data.splitlines()

            def part_1(self):
                return "solution for part 1"

            def part_2(self):
                return "solution for part 2"

    Or using slice syntax:
        class Solution(Advent[2022:1]):
            ...

    Options:
        - autorun: If True (default), runs solutions immediately on subclass creation
        - example: If True, uses example data instead of real puzzle input
        - offline: If True, only uses cached data (fails if not cached)
    """

    def __init_subclass__(
        cls,
        *,
        year: int | None = None,
        day: int | None = None,
        autorun: bool = True,
        example: bool = False,
        offline: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init_subclass__(**kwargs)

        msg = "Provide exactly one {arg} through subclass kwargs or getitem syntax"
        _year: int = not_both_provided_but_one(year, cls.__year__, msg.format(arg="year"))
        _day: int = not_both_provided_but_one(day, cls.__day__, msg.format(arg="day"))

        # Reset class attributes for next use
        cls.__year__ = None
        cls.__day__ = None

        if not autorun:
            return

        if example:
            data = get_example_data(_year, _day)
        elif offline:
            data = get(_year, _day)
            if data is None:
                raise DataNotFoundError(f"No cached data found for {_year} day {_day}")
        else:
            data = getch(_year, _day)

        cls(data).run_solutions()

    def __init__(self, data: str) -> None:
        """Initialize with puzzle input data. Override this to parse your input."""

    def run_solutions(self) -> None:
        """Run and benchmark both solution parts."""
        benchmark_and_print(self.part_1)
        benchmark_and_print(self.part_2)

    def part_1(self) -> Any:
        """Override to implement part 1 solution."""
        return NotImplemented

    def part_2(self) -> Any:
        """Override to implement part 2 solution."""
        return NotImplemented
