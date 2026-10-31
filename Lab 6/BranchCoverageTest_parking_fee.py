"""Branch coverage tests for parking_fee.py.

Goal: make every decision (if / elif / else, and each side of a compound
condition) evaluate to both True and False at least once.
"""
import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


# ======================= parking_fee =======================

# --- vehicle not in HOURLY_RATE: True / False ---
def test_unknown_vehicle_raises():
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee("bus", 60, False, False)


# --- minutes < 0: True / False (boundary at 0) ---
def test_negative_minutes_raises():
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", -1, False, False)


def test_zero_minutes_is_free():
    assert parking_fee("car", 0, False, False) == 0


# --- minutes <= 30: True / False (boundary at 30 / 31) ---
def test_free_short_stay():
    assert parking_fee("car", 20, False, False) == 0


def test_exactly_30_minutes_is_free():
    assert parking_fee("bike", 30, False, False) == 0


def test_31_minutes_is_charged_one_hour():
    assert parking_fee("bike", 31, False, False) == 10


# --- minutes % 60 != 0: True (round up) / False (exact hours) ---
def test_partial_hour_rounds_up():
    # 90 min -> 2 hours * 30
    assert parking_fee("car", 90, False, False) == 60


def test_exact_hours_not_rounded():
    # 120 min -> exactly 2 hours * 30
    assert parking_fee("car", 120, False, False) == 60


# --- is_ev and vehicle != "truck" ---
def test_ev_car_gets_half_price():
    assert parking_fee("car", 120, True, False) == 30


def test_ev_bike_gets_half_price():
    # 60 min -> 1 hour * 10 = 10, halved -> 5
    assert parking_fee("bike", 60, True, False) == 5


def test_ev_truck_gets_no_discount():
    # is_ev True but vehicle == "truck" -> condition False
    assert parking_fee("truck", 60, True, False) == 60


def test_non_ev_truck_full_price():
    # is_ev False (short-circuit) -> condition False
    assert parking_fee("truck", 150, False, False) == 180


# --- lost_ticket: True / False ---
def test_lost_ticket_adds_penalty():
    assert parking_fee("car", 60, False, True) == 230


def test_lost_ticket_on_free_stay():
    assert parking_fee("car", 10, False, True) == 200


def test_ev_and_lost_ticket_combined():
    # 2h * 30 = 60 -> EV half 30 -> +200 = 230
    assert parking_fee("car", 90, True, True) == 230


# ======================= find_slot =======================

# --- free_slots <= 0: True / False (boundary at 0 / 1) ---
def test_parking_full_zero_slots():
    assert find_slot("car", 0, False) == "full"


def test_parking_full_negative_slots():
    assert find_slot("bike", -2, True) == "full"


def test_one_free_slot_not_full():
    assert find_slot("car", 1, False) == "any floor"


# --- is_disabled: True / False ---
def test_disabled_gets_ground_floor():
    assert find_slot("car", 3, True) == "ground floor"


def test_disabled_truck_still_ground_floor():
    assert find_slot("truck", 3, True) == "ground floor"


# --- vehicle == "truck": True / False ---
def test_truck_goes_to_basement():
    assert find_slot("truck", 3, False) == "basement"


def test_any_floor():
    assert find_slot("car", 5, False) == "any floor"


def test_bike_any_floor():
    assert find_slot("bike", 5, False) == "any floor"


# ======================= monthly_pass =======================

# --- if bike / elif car / else ---
def test_bike_pass_non_resident():
    assert monthly_pass("bike", False) == 500


def test_bike_pass_resident():
    # 500 - 500 // 5 = 400
    assert monthly_pass("bike", True) == 400


def test_car_pass_non_resident():
    assert monthly_pass("car", False) == 1500


def test_car_pass_resident():
    # 1500 - 1500 // 5 = 1200
    assert monthly_pass("car", True) == 1200


@pytest.mark.parametrize("vehicle", ["truck", "bus"])
def test_no_pass_for_other_vehicles(vehicle):
    with pytest.raises(ValueError, match="no pass for this vehicle"):
        monthly_pass(vehicle, True)
