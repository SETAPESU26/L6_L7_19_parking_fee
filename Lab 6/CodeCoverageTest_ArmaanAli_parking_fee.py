"""Code coverage tests submitted by Armaan Ali (PES2UG24CS083)."""

import pytest

from parking_fee import find_slot, monthly_pass, parking_fee


def test_unknown_vehicle_is_rejected():
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee("scooter", 45, False, False)


def test_negative_duration_is_rejected():
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", -1, False, False)


def test_short_stay_is_free():
    assert parking_fee("car", 30, False, False) == 0


def test_partial_hour_ev_with_lost_ticket():
    assert parking_fee("car", 61, True, True) == 230


def test_exact_hour_and_truck_ev_exemption():
    assert parking_fee("truck", 60, True, False) == 60


def test_slot_is_full():
    assert find_slot("car", 0, False) == "full"


def test_disabled_slot_is_on_ground_floor():
    assert find_slot("bike", 2, True) == "ground floor"


def test_truck_slot_is_in_basement():
    assert find_slot("truck", 2, False) == "basement"


def test_regular_slot_can_be_on_any_floor():
    assert find_slot("car", 5, False) == "any floor"


def test_resident_bike_monthly_pass():
    assert monthly_pass("bike", True) == 400


def test_resident_car_monthly_pass():
    assert monthly_pass("car", True) == 1200


def test_unsupported_monthly_pass_is_rejected():
    with pytest.raises(ValueError, match="no pass for this vehicle"):
        monthly_pass("truck", True)
