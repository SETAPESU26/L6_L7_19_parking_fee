import re

from hypothesis import example, given, strategies as st

from parking_fee import RATES, format_plate, hourly_rate, minutes_parked

# Anything that is not a string: the functions must cope with these too.
NON_STRINGS = st.one_of(
    st.none(),
    st.integers(),
    st.floats(allow_nan=True),
    st.booleans(),
    st.binary(),
    st.lists(st.integers()),
)

PLATE_PATTERN = re.compile(r"[A-Z]{2} \d{2} [A-Z]{1,2} \d{4}", re.ASCII)


# ---------------------------------------------------------------------------
# 1. "Does it crash?" tests: the contract is that the functions never raise.
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
@example("")
@example("09:30")
@example("9am-5pm")
@example("-")
def test_minutes_parked_no_crash(s):
    try:
        minutes_parked(s)
    except Exception as e:
        assert False, f"minutes_parked crashed with: {e!r}"


@given(st.text() | st.none())
@example("")
@example("scooter")
@example(None)
def test_hourly_rate_no_crash(s):
    try:
        hourly_rate(s)
    except Exception as e:
        assert False, f"hourly_rate crashed with: {e!r}"


@given(st.text() | st.none())
@example("")
@example("ka01")
@example(None)
def test_format_plate_no_crash(s):
    try:
        format_plate(s)
    except Exception as e:
        assert False, f"format_plate crashed with: {e!r}"


@given(NON_STRINGS)
def test_all_functions_survive_non_string_input(x):
    for fn in (minutes_parked, hourly_rate, format_plate):
        try:
            result = fn(x)
        except Exception as e:
            assert False, f"{fn.__name__} crashed on {x!r} with: {e!r}"
        assert result is None, f"{fn.__name__}({x!r}) should reject non-strings"


# ---------------------------------------------------------------------------
# 2. Correctness properties for minutes_parked
# ---------------------------------------------------------------------------

times = st.tuples(
    st.integers(0, 23), st.integers(0, 59), st.integers(0, 23), st.integers(0, 59)
)


@given(times)
def test_minutes_parked_valid_range_is_correct(t):
    h1, m1, h2, m2 = t
    start, end = h1 * 60 + m1, h2 * 60 + m2
    result = minutes_parked(f"{h1:02d}:{m1:02d}-{h2:02d}:{m2:02d}")
    if end >= start:
        assert result == end - start
        assert 0 <= result < 24 * 60
    else:
        assert result is None  # exit before entry is invalid


@given(st.integers(24, 99) | st.integers(-99, -1), st.integers(0, 59))
def test_minutes_parked_rejects_out_of_range_hours(h, m):
    assert minutes_parked(f"{h}:{m:02d}-23:59") is None


@given(st.integers(0, 23), st.integers(60, 99))
def test_minutes_parked_rejects_out_of_range_minutes(h, m):
    assert minutes_parked(f"{h:02d}:{m}-23:59") is None


@given(st.text())
def test_minutes_parked_result_is_none_or_valid_duration(s):
    result = minutes_parked(s)
    assert result is None or (isinstance(result, int) and 0 <= result < 24 * 60)


# ---------------------------------------------------------------------------
# 3. Correctness properties for hourly_rate
# ---------------------------------------------------------------------------

def _mangle_case(name, flips):
    return "".join(c.upper() if f else c.lower() for c, f in zip(name, flips))


@given(
    st.sampled_from(sorted(RATES)),
    st.lists(st.booleans(), min_size=5, max_size=5),
    st.sampled_from(["", " ", "  ", "\t", "\n"]),
    st.sampled_from(["", " ", "  ", "\t", "\n"]),
)
def test_hourly_rate_is_case_and_whitespace_insensitive(name, flips, pre, post):
    text = pre + _mangle_case(name, flips) + post
    assert hourly_rate(text) == RATES[name]


@given(st.text())
def test_hourly_rate_unknown_vehicle_is_none(s):
    result = hourly_rate(s)
    key = s.strip().lower() if s.isascii() else None
    if key in RATES:
        assert result == RATES[key]
    else:
        assert result is None


@given(st.text())
def test_hourly_rate_result_is_none_or_known_rate(s):
    assert hourly_rate(s) in set(RATES.values()) | {None}


# ---------------------------------------------------------------------------
# 4. Correctness properties for format_plate
# ---------------------------------------------------------------------------

plates = st.builds(
    lambda state, dist, series, num: f"{state}{dist:02d}{series}{num:04d}",
    st.text("ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=2, max_size=2),
    st.integers(0, 99),
    st.text("ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=2),
    st.integers(0, 9999),
)


@given(plates, st.booleans())
def test_format_plate_valid_plates_are_formatted(plate, lower):
    raw = plate.lower() if lower else plate
    result = format_plate(raw)
    assert result is not None
    assert PLATE_PATTERN.fullmatch(result)
    assert result.replace(" ", "") == plate


@given(st.text())
def test_format_plate_result_is_none_or_well_formed(s):
    result = format_plate(s)
    assert result is None or PLATE_PATTERN.fullmatch(result)


@given(plates, st.integers(1, 5))
def test_format_plate_rejects_truncated_plates(plate, cut):
    assert format_plate(plate[:-cut]) is None


@given(plates, st.text("0123456789", min_size=1, max_size=3))
def test_format_plate_rejects_overlong_plates(plate, extra):
    assert format_plate(plate + extra) is None
