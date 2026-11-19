import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


@pytest.mark.parametrize(
    ("vehicle", "minutes", "expected"),
    [
        ("bike", 30, 0),
        ("bike", 31, 10),
        ("car", 60, 30),
        ("car", 61, 60),
        ("truck", 90, 120),
    ],
)
def test_parking_fee_by_vehicle_and_rounded_hours(vehicle, minutes, expected):
    assert parking_fee(vehicle, minutes, False, False) == expected


@pytest.mark.parametrize(
    ("vehicle", "minutes", "expected"),
    [
        ("car", 61, 30),
        ("bike", 31, 5),
        ("truck", 61, 120),
    ],
)
def test_ev_discount_applies_except_to_trucks(vehicle, minutes, expected):
    assert parking_fee(vehicle, minutes, True, False) == expected


def test_lost_ticket_fee_is_added_to_free_stay():
    assert parking_fee("car", 20, False, True) == 200


@pytest.mark.parametrize(
    ("vehicle", "minutes", "is_ev", "expected"),
    [
        ("car", 61, False, 260),
        ("car", 61, True, 230),
    ],
)
def test_lost_ticket_fee_is_added_after_hourly_fee(vehicle, minutes, is_ev, expected):
    assert parking_fee(vehicle, minutes, is_ev, True) == expected


@pytest.mark.parametrize("vehicle", ["plane", "", None])
def test_unknown_vehicle_is_rejected(vehicle):
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee(vehicle, 20, False, False)


def test_negative_duration_is_rejected():
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", -1, False, False)


@pytest.mark.parametrize(
    ("vehicle", "free_slots", "is_disabled", "expected"),
    [
        ("car", 0, False, "full"),
        ("car", 5, True, "ground floor"),
        ("truck", 5, False, "basement"),
        ("car", 5, False, "any floor"),
    ],
)
def test_find_slot(vehicle, free_slots, is_disabled, expected):
    assert find_slot(vehicle, free_slots, is_disabled) == expected


@pytest.mark.parametrize(
    ("vehicle", "is_resident", "expected"),
    [
        ("bike", False, 500),
        ("bike", True, 400),
        ("car", False, 1500),
        ("car", True, 1200),
    ],
)
def test_monthly_pass_prices(vehicle, is_resident, expected):
    assert monthly_pass(vehicle, is_resident) == expected


def test_monthly_pass_rejects_trucks():
    with pytest.raises(ValueError, match="no pass for this vehicle"):
        monthly_pass("truck", False)
