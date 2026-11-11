"""Lab 6 - Code (line) coverage tests for parking_fee.py

Goal: execute every line of parking_fee.py at least once (>= 90% line coverage).

Run:
    coverage run --include=parking_fee.py -m pytest CodeCoverageTest_parking_fee_application.py
    coverage report -m
"""
import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


# ---------- parking_fee ----------
def test_free_short_stay():
    assert parking_fee("car", 20, False, False) == 0


def test_unknown_vehicle_raises():
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee("cycle", 60, False, False)


def test_negative_minutes_raises():
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", -5, False, False)


def test_paid_stay_rounds_up_to_next_hour():
    # 90 minutes -> 2 billable hours -> 2 * 30 = 60
    assert parking_fee("car", 90, False, False) == 60


def test_ev_car_gets_half_fee():
    # 60 for 2 hours, halved -> 30
    assert parking_fee("car", 90, True, False) == 30


def test_lost_ticket_adds_penalty():
    assert parking_fee("bike", 10, False, True) == 200


# ---------- find_slot ----------
def test_slot_full():
    assert find_slot("car", 0, False) == "full"


def test_slot_any_floor():
    assert find_slot("car", 5, False) == "any floor"


def test_slot_disabled_ground_floor():
    assert find_slot("car", 5, True) == "ground floor"


def test_slot_truck_basement():
    assert find_slot("truck", 5, False) == "basement"


# ---------- monthly_pass ----------
def test_monthly_pass_bike():
    assert monthly_pass("bike", False) == 500


def test_monthly_pass_car_resident_discount():
    # 1500 - 300 = 1200
    assert monthly_pass("car", True) == 1200


def test_monthly_pass_invalid_vehicle_raises():
    with pytest.raises(ValueError, match="no pass"):
        monthly_pass("truck", False)
