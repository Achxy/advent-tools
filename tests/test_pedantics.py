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
