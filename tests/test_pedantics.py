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

import pytest

from advent._pedantics import (
    check_if_can_be_well_formatted,
    check_if_valid_day,
    check_if_valid_year,
    check_if_viable_date,
    check_type,
    not_both_provided_but_one,
)


def test_check_if_can_be_well_formatted() -> None:
    assert check_if_can_be_well_formatted("{a}, lorem ipsum pq{b}rs", "a", "b") is None
    assert check_if_can_be_well_formatted("{a}{b}", "a", "b") is None
    assert check_if_can_be_well_formatted("{a b}", "a b") is None
    assert check_if_can_be_well_formatted("{a}, lorem ipsum pq{b}rs", "a", "b", "c") is None
    with pytest.raises(ValueError):
        check_if_can_be_well_formatted("djf {a} {n}", "", "")
    with pytest.raises(ValueError):
        check_if_can_be_well_formatted("{a}, 3042usd hbjaus8sdvjan al{n}kd", "a")
    with pytest.raises(ValueError):
        check_if_can_be_well_formatted("{} {a}, lorem ipsum pq{b}rs", "a", "b", "c")


def test_check_if_valid_day() -> None:
    assert check_if_valid_day(1) == 1
    assert check_if_valid_day(25) == 25
    assert check_if_valid_day(13) == 13
    with pytest.raises(ValueError):
        check_if_valid_day(0)
    with pytest.raises(ValueError):
        check_if_valid_day(26)
    with pytest.raises(ValueError):
        check_if_valid_day(-1)
    with pytest.raises(TypeError):
        check_if_valid_day("1")  # type: ignore


def test_check_if_valid_year() -> None:
    assert check_if_valid_year(2015) == 2015
    assert check_if_valid_year(2022) == 2022
    assert check_if_valid_year(2024) == 2024
    with pytest.raises(ValueError):
        check_if_valid_year(2014)
    with pytest.raises(ValueError):
        check_if_valid_year(2025)
    with pytest.raises(TypeError):
        check_if_valid_year("2022")  # type: ignore


def test_check_if_viable_date() -> None:
    # 8:00 AM UTC-5 on 15st Dec 2022
    mock_datetime_1 = datetime(2022, 12, 15, 8, 0, 0, tzinfo=timezone(timedelta(hours=-5)))  # type: ignore
    assert check_if_viable_date(2022, 1) is None
    assert check_if_viable_date(2022, 25) is None
    assert check_if_viable_date(2015, 6) is None
    # TODO: Complete this (mock datetime.now() to return mock_datetime_1)


def test_check_type() -> None:
    class StrSub(str): ...

    assert check_type("a", 1, int) == 1
    assert check_type("a", 1, int, strict=True) == 1
    assert check_type("a", 1, int, strict=False) == 1
    assert check_type("a", "1", str) == "1"
    assert check_type("a", StrSub("1"), str) == StrSub("1")
    assert check_type("a", StrSub("1"), str, strict=False) == StrSub("1")
    assert check_type("a", StrSub("1"), StrSub, strict=True) == StrSub("1")
    with pytest.raises(TypeError):
        check_type("a", 1, str)
    with pytest.raises(TypeError):
        check_type("a", 1.0, int)
    with pytest.raises(TypeError):
        check_type("a", StrSub("1"), str, strict=True)
    with pytest.raises(TypeError):
        check_type("a", "1", StrSub)


def test_not_both_provided_but_one() -> None:
    assert not_both_provided_but_one(1, None) == 1
    assert not_both_provided_but_one(None, 2) == 2
    with pytest.raises(ValueError):
        not_both_provided_but_one(1, 2)
    with pytest.raises(ValueError):
        not_both_provided_but_one(1, 1)
    with pytest.raises(ValueError):
        not_both_provided_but_one(0, 0)
    with pytest.raises(ValueError):
        not_both_provided_but_one(False, False)
    with pytest.raises(ValueError):
        not_both_provided_but_one(True, True)
    with pytest.raises(ValueError):
        not_both_provided_but_one(None, None)
    with pytest.raises(ValueError):
        not_both_provided_but_one(1, 2, "Provide only one!!!")
