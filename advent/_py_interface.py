from __future__ import annotations

from functools import partial
from typing import Any, Callable

from _config_reader import Configuration
from _pedantics import check_if_viable_date

from advent._data_handle import get, get_example_data, getch


class _InstantiatorFromSlice(type):
    def __getitem__(self, date: slice[int, int, None]) -> Callable[..., type]:
        if date.step is not None:
            name = self.__name__
            raise ValueError(f"Please instantiate in following format {name}[YEAR:DAY]")
        return partial(self, year=date.start, day=date.stop)


class Advent(metaclass=_InstantiatorFromSlice):
    def __init_subclass__(
        cls, *, year: int, day: int, autorun: bool = True, example: bool = False, offline: bool = False, **kwargs
    ):
        if autorun:
            if example:
                return cls(get_example_data(year, day)).run_solutions()
            if offline:
                if (data := get(year, day)) is not None:
                    return cls(data).run_solutions()
                raise ValueError(f"No offline data found for year {year}, day {day}")
            return cls(getch(year, day)).run_solutions()

    def __init__(self, data: str) -> None:
        pass

    def run_solutions(self):
        self.part_1()
        self.part_2()

    def part_1(self) -> Any:
        return NotImplemented

    def part_2(self) -> Any:
        return NotImplemented


class Foo(metaclass=_InstantiatorFromSlice):
    def __init__(self, *, year: int, day: int, test: bool = False):
        self.year = year
        self.day = day

    def say(self):
        print(f"Year: {self.year}, Day: {self.day}")


Foo[2021:1]().say()
