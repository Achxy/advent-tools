from __future__ import annotations

from functools import partial
from typing import Any, Callable

from _config_reader import Configuration
from _pedantics import check_if_viable_date, not_both_provided_but_one

from advent._data_handle import get, get_example_data, getch
from _typeshack import FakeGenericForGetItemSupport

class _InstantiatorFromSlice(type):
    def __getitem__(self, date: slice[int, int, None]) -> Callable[..., type]:
        if date.step is not None:
            name = self.__name__
            raise ValueError(f"Please instantiate in following format {name}[YEAR:DAY]")
        self.__year__: int = date.start
        self.__day__: int = date.stop
        return self


class Advent(FakeGenericForGetItemSupport, metaclass=_InstantiatorFromSlice):
    def __init_subclass__(
        cls, *, year: int | None = None, day: int | None = None, autorun: bool = True, example: bool = False, offline: bool = False, **kwargs
    ):
        _year: int = not_both_provided_but_one(year, cls.__year__, "Provide exactly one year through subclass kwargs or getitem syntax")
        _day: int = not_both_provided_but_one(day, cls.__day__, "Provide exactly one day through subclass kwargs or getitem syntax")
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
        self.part_1()
        self.part_2()

    def part_1(self) -> Any:
        return NotImplemented

    def part_2(self) -> Any:
        return NotImplemented


class Foo(Advent[2021:1]):
    def __init__(self, data: str) -> None:
        print(data.splitlines()[0])
