"""Branch coverage tests submitted by Armaan Ali (PES2UG24CS083)."""

import pytest

from parking_fee import find_slot, monthly_pass, parking_fee


def test_parking_fee_validation_branches():
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee("scooter", 45, False, False)
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", -1, False, False)


def test_parking_fee_duration_and_rounding_branches():
    assert parking_fee("car", 30, False, False) == 0
    assert parking_fee("bike", 60, False, False) == 10
    assert parking_fee("car", 61, False, False) == 60


def test_ev_and_lost_ticket_branches():
    assert parking_fee("car", 60, True, False) == 15
    assert parking_fee("truck", 60, True, False) == 60
    assert parking_fee("bike", 60, False, True) == 210


def test_slot_assignment_branches():
    assert find_slot("car", 0, False) == "full"
    assert find_slot("bike", 2, True) == "ground floor"
    assert find_slot("truck", 2, False) == "basement"
    assert find_slot("car", 2, False) == "any floor"


def test_monthly_pass_vehicle_and_residency_branches():
    assert monthly_pass("bike", True) == 400
    assert monthly_pass("bike", False) == 500
    assert monthly_pass("car", True) == 1200
    assert monthly_pass("car", False) == 1500
    with pytest.raises(ValueError, match="no pass for this vehicle"):
        monthly_pass("truck", False)
