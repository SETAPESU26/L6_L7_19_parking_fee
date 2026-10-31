"""Code (line) coverage tests for parking_fee.py.

Goal: execute every line of the module at least once.
"""
import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


# ---------- parking_fee ----------

def test_free_short_stay():
    assert parking_fee("car", 20, False, False) == 0


def test_unknown_vehicle_raises():
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee("bus", 60, False, False)


def test_negative_minutes_raises():
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", -5, False, False)


def test_partial_hour_rounds_up_with_ev_and_lost_ticket():
    # 90 min -> 2 hours * 30 = 60, EV car halves -> 30, lost ticket +200 -> 230
    assert parking_fee("car", 90, True, True) == 230


# ---------- find_slot ----------

def test_any_floor():
    assert find_slot("car", 5, False) == "any floor"


def test_parking_full():
    assert find_slot("car", 0, False) == "full"


def test_disabled_gets_ground_floor():
    assert find_slot("car", 3, True) == "ground floor"


def test_truck_goes_to_basement():
    assert find_slot("truck", 3, False) == "basement"


# ---------- monthly_pass ----------

def test_bike_pass_resident():
    # 500 - 500 // 5 = 400
    assert monthly_pass("bike", True) == 400


def test_car_pass():
    assert monthly_pass("car", False) == 1500


def test_truck_has_no_pass():
    with pytest.raises(ValueError, match="no pass for this vehicle"):
        monthly_pass("truck", False)
