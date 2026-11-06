import re

RATES = {"bike": 10, "car": 30, "truck": 60}

# HH:MM with ASCII digits only (str.isdigit() would also accept things like '²' or Arabic digits)
TIME_RE = re.compile(r"([0-9]{1,2}):([0-9]{2})")
# Indian plate format: 2 letters, 2 digits, 2 letters, 4 digits  (e.g. KA01AB1234)
PLATE_RE = re.compile(r"[A-Za-z]{2}[0-9]{2}[A-Za-z]{2}[0-9]{4}")


def _to_minutes(t):
    """Convert 'HH:MM' to minutes since midnight, or None if invalid."""
    match = TIME_RE.fullmatch(t.strip())
    if not match:
        return None
    h, m = int(match.group(1)), int(match.group(2))
    if not (0 <= h <= 23 and 0 <= m <= 59):
        return None
    return h * 60 + m


def minutes_parked(times):
    """Return minutes between entry and exit ('HH:MM-HH:MM'), or None if input is invalid."""
    if not isinstance(times, str):
        return None
    parts = times.split('-')
    if len(parts) != 2:
        return None
    start = _to_minutes(parts[0])
    end = _to_minutes(parts[1])
    if start is None or end is None:
        return None
    if end < start:          # exit before entry is not a valid stay
        return None
    return end - start


def hourly_rate(vehicle):
    """Return the hourly rate for a vehicle type, or None if unknown/invalid."""
    if not isinstance(vehicle, str):
        return None
    return RATES.get(vehicle.strip().lower())


def format_plate(plate):
    """Return a plate formatted as 'KA 01 AB 1234', or None if invalid."""
    if not isinstance(plate, str):
        return None
    p = plate.strip().replace(" ", "")
    if not PLATE_RE.fullmatch(p):   # validate BEFORE upper(): 'ß'.upper() == 'SS' changes length
        return None
    p = p.upper()
    return p[0] + p[1] + " " + p[2:4] + " " + p[4:6] + " " + p[6:10]


def main():
    print("==== Running minutes_parked ====")
    user_input = input("Enter entry and exit time (e.g. 09:30-11:45): ")
    result = minutes_parked(user_input)
    print("Minutes Parked:", result if result is not None else "Invalid input")

    print("\n==== Running hourly_rate ====")
    user_input = input("Enter vehicle type (bike/car/truck): ")
    result = hourly_rate(user_input)
    print("Hourly Rate:", result if result is not None else "Invalid input")

    print("\n==== Running format_plate ====")
    user_input = input("Enter a number plate (e.g. ka01ab1234): ")
    result = format_plate(user_input)
    print("Formatted Plate:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
