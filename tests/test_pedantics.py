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


def test_check_if_can_be_well_formatted():
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


def test_check_if_valid_day():
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


def test_check_if_valid_year():
    assert check_if_valid_year(2015) == 2015
    assert check_if_valid_year(2022) == 2022
    assert check_if_valid_year(2024) == 2024
    with pytest.raises(ValueError):
        check_if_valid_year(2014)
    with pytest.raises(ValueError):
        check_if_valid_year(2025)
    with pytest.raises(TypeError):
        check_if_valid_year("2022")  # type: ignore


def test_check_if_viable_date():
    # 8:00 AM UTC-5 on 15st Dec 2022
    mock_datetime_1 = datetime(2022, 12, 15, 8, 0, 0, tzinfo=timezone(timedelta(hours=-5)))  # type: ignore
    assert check_if_viable_date(2022, 1) is None
    assert check_if_viable_date(2022, 25) is None
    assert check_if_viable_date(2015, 6) is None
    # TODO: Complete this (mock datetime.now() to return mock_datetime_1)


def test_check_type():
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
