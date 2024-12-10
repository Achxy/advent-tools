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

from __future__ import annotations

from typing import Any, Callable

from ._benchmark import benchmark_and_print
from ._data_handle import get, get_example_data, getch
from ._pedantics import not_both_provided_but_one
from ._typeshack import FakeGenericForGetItemSupport, FakeType


class _InstantiatorFromSlice(type):
    __year__: int | None = None
    __day__: int | None = None

    def __getitem__(self, date: slice[int, int, None]) -> Callable[..., type]:
        if date.step is not None:
            name = self.__name__
            raise ValueError(f"Please instantiate in following format {name}[YEAR:DAY]")
        self.__year__ = date.start
        self.__day__ = date.stop
        return self


class Advent(FakeGenericForGetItemSupport[FakeType], metaclass=_InstantiatorFromSlice):
    def __init_subclass__(
        cls,
        *,
        year: int | None = None,
        day: int | None = None,
        autorun: bool = True,
        example: bool = False,
        offline: bool = False,
        **kwargs: Any,
    ):
        msg = "Provide exactly one {arg} through subclass kwargs or getitem syntax"
        _year: int = not_both_provided_but_one(year, cls.__year__, msg.format(arg="year"))
        _day: int = not_both_provided_but_one(day, cls.__day__, msg.format(arg="day"))
        if autorun:
            if example:
                return cls(get_example_data(_year, _day)).run_solutions()
            if offline:
                if (data := get(_year, _day)) is not None:
                    return cls(data).run_solutions()
                raise ValueError(f"No offline data found for year {year}, day {day}")
            return cls(getch(_year, _day)).run_solutions()

    def __init__(self, data: str) -> None:
        pass

    def run_solutions(self):
        benchmark_and_print(self.part_1)
        benchmark_and_print(self.part_2)

    def part_1(self) -> Any:
        return NotImplemented

    def part_2(self) -> Any:
        return NotImplemented
