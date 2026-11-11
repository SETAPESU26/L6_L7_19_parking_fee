"""Lab 6 - Branch coverage tests for parking_fee.py

Goal: make every decision (if / elif) evaluate to both True and False
(>= 90% branch coverage), including boundary values.

Run:
    coverage run --branch --include=parking_fee.py -m pytest BranchCoverageTest_parking_fee_application.py
    coverage report -m
"""
import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


# ---------- parking_fee: validation branches ----------
def test_known_vehicle_is_accepted():
    # `vehicle not in HOURLY_RATE` -> False
    assert parking_fee("bike", 60, False, False) == 10


def test_unknown_vehicle_raises():
    # `vehicle not in HOURLY_RATE` -> True
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee("cycle", 60, False, False)


def test_negative_minutes_raises():
    # `minutes < 0` -> True
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", -1, False, False)


def test_zero_minutes_is_valid_and_free():
    # `minutes < 0` -> False (boundary), `minutes <= 30` -> True
    assert parking_fee("car", 0, False, False) == 0


# ---------- parking_fee: free-period boundary (minutes <= 30) ----------
def test_exactly_30_minutes_is_free():
    assert parking_fee("car", 30, False, False) == 0


def test_31_minutes_is_charged_one_hour():
    # `minutes <= 30` -> False; 31 % 60 != 0 -> True
    assert parking_fee("car", 31, False, False) == 30


# ---------- parking_fee: hour rounding (minutes % 60 != 0) ----------
def test_exact_hour_no_round_up():
    # `minutes % 60 != 0` -> False
    assert parking_fee("car", 60, False, False) == 30


def test_partial_hour_rounds_up():
    # `minutes % 60 != 0` -> True : 61 min -> 2 hours
    assert parking_fee("car", 61, False, False) == 60


def test_each_vehicle_rate():
    assert parking_fee("bike", 120, False, False) == 20
    assert parking_fee("car", 120, False, False) == 60
    assert parking_fee("truck", 120, False, False) == 120


# ---------- parking_fee: EV discount (is_ev and vehicle != "truck") ----------
def test_ev_car_discount():
    # is_ev True and vehicle != truck True
    assert parking_fee("car", 61, True, False) == 30


def test_ev_bike_discount_uses_integer_division():
    # 10 // 2 = 5
    assert parking_fee("bike", 31, True, False) == 5


def test_ev_truck_gets_no_discount():
    # is_ev True but vehicle != truck False
    assert parking_fee("truck", 90, True, False) == 120


def test_non_ev_gets_no_discount():
    # is_ev False
    assert parking_fee("car", 61, False, False) == 60


# ---------- parking_fee: lost ticket ----------
def test_lost_ticket_adds_penalty_to_paid_stay():
    # lost_ticket True
    assert parking_fee("car", 61, False, True) == 260


def test_lost_ticket_on_free_stay():
    assert parking_fee("car", 10, False, True) == 200


def test_ticket_present_no_penalty():
    # lost_ticket False
    assert parking_fee("car", 10, False, False) == 0


def test_ev_discount_then_lost_ticket():
    # discount applied before the penalty: 60 // 2 + 200
    assert parking_fee("car", 61, True, True) == 230


# ---------- find_slot ----------
def test_slot_full_when_no_free_slots():
    assert find_slot("car", 0, False) == "full"


def test_slot_full_when_negative_free_slots():
    assert find_slot("car", -3, False) == "full"


def test_slot_full_overrides_disabled():
    assert find_slot("car", 0, True) == "full"


def test_slot_disabled_gets_ground_floor():
    assert find_slot("car", 5, True) == "ground floor"


def test_slot_disabled_truck_still_ground_floor():
    assert find_slot("truck", 5, True) == "ground floor"


def test_slot_truck_goes_to_basement():
    assert find_slot("truck", 5, False) == "basement"


def test_slot_any_floor_for_car_and_bike():
    assert find_slot("car", 5, False) == "any floor"
    assert find_slot("bike", 1, False) == "any floor"


# ---------- monthly_pass ----------
def test_pass_bike_non_resident():
    assert monthly_pass("bike", False) == 500


def test_pass_bike_resident():
    assert monthly_pass("bike", True) == 400


def test_pass_car_non_resident():
    assert monthly_pass("car", False) == 1500


def test_pass_car_resident():
    assert monthly_pass("car", True) == 1200


def test_pass_truck_not_available():
    with pytest.raises(ValueError, match="no pass"):
        monthly_pass("truck", False)


def test_pass_unknown_vehicle_not_available():
    with pytest.raises(ValueError, match="no pass"):
        monthly_pass("cycle", True)
