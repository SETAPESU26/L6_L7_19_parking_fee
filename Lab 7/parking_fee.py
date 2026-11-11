import re

RATES = {"bike": 10, "car": 30, "truck": 60}

# "H:MM-H:MM" / "HH:MM-HH:MM", ASCII digits only (int() would also accept
# things like Arabic-Indic digits, "+5" or "1_0", which we do not want).
_TIME_RANGE = re.compile(r"(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})", re.ASCII)

# Indian style plate: 2 letters, 2 digits, 1-2 letters, 4 digits (KA01AB1234).
_PLATE = re.compile(r"([A-Z]{2})(\d{2})([A-Z]{1,2})(\d{4})", re.ASCII | re.IGNORECASE)


def minutes_parked(times):
    """Return minutes between entry and exit for a string like "09:30-11:45".

    Returns None for anything invalid: non-strings, wrong format, hours not in
    0-23, minutes not in 0-59, or an exit time earlier than the entry time.
    """
    if not isinstance(times, str):
        return None
    match = _TIME_RANGE.fullmatch(times.strip())
    if match is None:
        return None
    h1, m1, h2, m2 = (int(g) for g in match.groups())
    if h1 > 23 or h2 > 23 or m1 > 59 or m2 > 59:
        return None
    duration = (h2 * 60 + m2) - (h1 * 60 + m1)
    if duration < 0:
        return None
    return duration


def hourly_rate(vehicle):
    """Return the hourly rate for "bike", "car" or "truck" (any case, any
    surrounding whitespace). Returns None for unknown or non-string input."""
    if not isinstance(vehicle, str):
        return None
    # ASCII only: some Unicode characters lower-case onto ASCII letters
    # (e.g. the Kelvin sign), which would let look-alikes through.
    if not vehicle.isascii():
        return None
    return RATES.get(vehicle.strip().lower())


def format_plate(plate):
    """Format a plate like "ka01ab1234" as "KA 01 AB 1234".

    Spaces and hyphens in the input are ignored. Returns None if the input is
    not a string or is not a well-formed plate.
    """
    if not isinstance(plate, str):
        return None
    cleaned = re.sub(r"[\s-]", "", plate)
    match = _PLATE.fullmatch(cleaned)
    if match is None:
        return None
    return " ".join(match.groups()).upper()


def main():
    print("==== Running minutes_parked ====")
    user_input = input("Enter entry and exit time (e.g. 09:30-11:45): ")
    result = minutes_parked(user_input)
    if result is None:
        print("Invalid time range. Use HH:MM-HH:MM with exit not before entry.")
    else:
        print("Minutes Parked:", result)

    print("\n==== Running hourly_rate ====")
    user_input = input("Enter vehicle type (bike/car/truck): ")
    result = hourly_rate(user_input)
    if result is None:
        print("Unknown vehicle type. Choose bike, car or truck.")
    else:
        print("Hourly Rate:", result)

    print("\n==== Running format_plate ====")
    user_input = input("Enter a number plate (e.g. ka01ab1234): ")
    result = format_plate(user_input)
    if result is None:
        print("Invalid number plate. Expected something like KA01AB1234.")
    else:
        print("Formatted Plate:", result)


if __name__ == "__main__":
    main()
