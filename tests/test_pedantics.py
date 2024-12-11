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
    