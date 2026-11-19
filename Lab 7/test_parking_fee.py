import string

import pytest
from hypothesis import given, strategies as st
from parking_fee import minutes_parked, hourly_rate, format_plate


@given(st.integers(min_value=0, max_value=1439), st.integers(min_value=0, max_value=1439))
def test_minutes_parked_valid_range(entry, exit_time):
    times = (
        f"{entry // 60:02}:{entry % 60:02}"
        f"-{exit_time // 60:02}:{exit_time % 60:02}"
    )
    assert minutes_parked(times) == (exit_time - entry) % (24 * 60)


@given(st.text().filter(lambda value: "-" not in value))
def test_minutes_parked_rejects_inputs_without_separator(value):
    with pytest.raises(ValueError):
        minutes_parked(value)


@pytest.mark.parametrize(
    "value",
    [None, 42, "", "09:00", "24:00-10:00", "09:60-10:00", "09:00-10:00-11:00"],
)
def test_minutes_parked_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        minutes_parked(value)


@given(st.sampled_from(["bike", "car", "truck"]))
def test_hourly_rate_returns_rate_for_supported_vehicle(vehicle):
    expected = {"bike": 10, "car": 30, "truck": 60}[vehicle]
    assert hourly_rate(vehicle) == expected


@given(
    st.text().filter(
        lambda value: value.strip().lower() not in {"bike", "car", "truck"}
    )
)
def test_hourly_rate_rejects_unsupported_names(vehicle):
    with pytest.raises(ValueError):
        hourly_rate(vehicle)


@pytest.mark.parametrize("vehicle", [None, 123])
def test_hourly_rate_rejects_non_strings(vehicle):
    with pytest.raises(ValueError):
        hourly_rate(vehicle)


@given(
    st.text(alphabet=string.ascii_letters, min_size=2, max_size=2),
    st.text(alphabet=string.digits, min_size=2, max_size=2),
    st.text(alphabet=string.ascii_letters, min_size=2, max_size=2),
    st.text(alphabet=string.digits, min_size=4, max_size=4),
)
def test_format_plate_formats_valid_plates(region, number, series, serial):
    plate = region + number + series + serial
    assert format_plate(plate.lower()) == (
        f"{region.upper()} {number} {series.upper()} {serial}"
    )


@given(st.text(max_size=9))
def test_format_plate_rejects_short_plates(plate):
    with pytest.raises(ValueError):
        format_plate(plate)


@pytest.mark.parametrize("plate", [None, 1234567890, "KA01AB12X4", "KA01AB12345"])
def test_format_plate_rejects_invalid_plate_values(plate):
    with pytest.raises(ValueError):
        format_plate(plate)
