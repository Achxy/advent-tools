from __future__ import annotations

from functools import partial

from _config_reader import Configuration
from _pedantics import check_if_viable_date


class _InstantiatorFromSlice(type):
    def __getitem__(self, date: slice[int, int, None]):
        if date.step is not None:
            name = self.__name__
            raise ValueError(f"Please instantiate in following format {name}[YEAR:DAY]")
        return partial(self, year=date.start, day=date.stop)


class Advent(metaclass=_InstantiatorFromSlice):
    def __init__(self, *, year: int, day: int, example: bool = False, offline: bool = False):
        check_if_viable_date(year, day)
        self.year = year
        self.day = day

    def say(self):
        print(f"Year: {self.year}, Day: {self.day}")


class Foo(metaclass=_InstantiatorFromSlice):
    def __init__(self, *, year: int, day: int, test: bool = False):
        self.year = year
        self.day = day

    def say(self):
        print(f"Year: {self.year}, Day: {self.day}")


Foo[2021:1]().say()
