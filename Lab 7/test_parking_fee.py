from hypothesis import given, strategies as st
from parking_fee import minutes_parked, hourly_rate, format_plate


# ---------- Fuzz tests: random / malformed input must never crash ----------

@given(st.text() | st.none())
def test_minutes_parked_no_crash(s):
    try:
        minutes_parked(s)
    except Exception as e:
        assert False, f"minutes_parked crashed with: {e!r}"


@given(st.text() | st.none())
def test_hourly_rate_no_crash(s):
    try:
        hourly_rate(s)
    except Exception as e:
        assert False, f"hourly_rate crashed with: {e!r}"


@given(st.text() | st.none())
def test_format_plate_no_crash(s):
    try:
        format_plate(s)
    except Exception as e:
        assert False, f"format_plate crashed with: {e!r}"


# ---------- Property tests: valid input must still give the right answer ----------

@given(st.integers(0, 23), st.integers(0, 59), st.integers(0, 23), st.integers(0, 59))
def test_minutes_parked_valid_times(h1, m1, h2, m2):
    start, end = h1 * 60 + m1, h2 * 60 + m2
    s = f"{h1:02d}:{m1:02d}-{h2:02d}:{m2:02d}"
    result = minutes_parked(s)
    if end >= start:
        assert result == end - start
    else:
        # exit before entry is invalid: must not return a negative duration
        assert result is None


@given(st.sampled_from(["bike", "car", "truck"]), st.sampled_from(["", " ", "  "]), st.booleans())
def test_hourly_rate_valid_vehicles(vehicle, pad, upper):
    v = vehicle.upper() if upper else vehicle
    assert hourly_rate(pad + v + pad) == {"bike": 10, "car": 30, "truck": 60}[vehicle]


@given(
    st.text("abcdefghijklmnopqrstuvwxyz", min_size=2, max_size=2),
    st.integers(0, 99),
    st.text("abcdefghijklmnopqrstuvwxyz", min_size=2, max_size=2),
    st.integers(0, 9999),
)
def test_format_plate_valid_plates(state, district, series, number):
    plate = f"{state}{district:02d}{series}{number:04d}"
    assert format_plate(plate) == f"{state.upper()} {district:02d} {series.upper()} {number:04d}"
