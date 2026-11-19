RATES = {"bike": 10, "car": 30, "truck": 60}


def minutes_parked(times):
    if not isinstance(times, str):
        raise ValueError("times must be a string")

    times = times.strip()
    parts = times.split("-")
    if len(parts) != 2:
        raise ValueError("times must use HH:MM-HH:MM format")

    def parse_time(value):
        fields = value.split(":")
        if (
            len(fields) != 2
            or any(len(field) != 2 or not field.isascii() or not field.isdigit() for field in fields)
        ):
            raise ValueError("time must use HH:MM format")
        hour, minute = map(int, fields)
        if hour > 23 or minute > 59:
            raise ValueError("time is outside the 24-hour clock")
        return hour * 60 + minute

    entry, exit_time = map(parse_time, parts)
    duration = exit_time - entry
    return duration if duration >= 0 else duration + 24 * 60


def hourly_rate(vehicle):
    if not isinstance(vehicle, str):
        raise ValueError("unknown vehicle")
    normalized_vehicle = vehicle.strip().lower()
    if normalized_vehicle not in RATES:
        raise ValueError("unknown vehicle")
    return RATES[normalized_vehicle]


def format_plate(plate):
    if not isinstance(plate, str):
        raise ValueError("plate must be a string")
    normalized_plate = plate.strip().upper()
    if (
        len(normalized_plate) != 10
        or not (
            normalized_plate[:2].isascii()
            and normalized_plate[:2].isalpha()
            and normalized_plate[2:4].isascii()
            and normalized_plate[2:4].isdigit()
            and normalized_plate[4:6].isascii()
            and normalized_plate[4:6].isalpha()
            and normalized_plate[6:10].isascii()
            and normalized_plate[6:10].isdigit()
        )
    ):
        raise ValueError("plate must use the LLDDLLDDDD format")
    return (
        normalized_plate[:2]
        + " "
        + normalized_plate[2:4]
        + " "
        + normalized_plate[4:6]
        + " "
        + normalized_plate[6:10]
    )


def main():
    print("==== Running minutes_parked ====")
    user_input = input("Enter entry and exit time (e.g. 09:30-11:45): ")
    result = minutes_parked(user_input)
    print("Minutes Parked:", result)

    print("\n==== Running hourly_rate ====")
    user_input = input("Enter vehicle type (bike/car/truck): ")
    result = hourly_rate(user_input)
    print("Hourly Rate:", result)

    print("\n==== Running format_plate ====")
    user_input = input("Enter a number plate (e.g. ka01ab1234): ")
    result = format_plate(user_input)
    print("Formatted Plate:", result)

if __name__ == "__main__":
    main()
