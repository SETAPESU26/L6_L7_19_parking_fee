# Parking Fee Labs Report

**Name:** Armaan Ali  
**SRN:** PES2UG24CS083  
**Repository:** [L6_L7_19_parking_fee](https://github.com/SETAPESU26/L6_L7_19_parking_fee)

## Deliverables

- **Lab 6:** Completed tests for parking fees, vehicle validation, EV and lost-ticket adjustments, slot assignment, and monthly passes. Added test and coverage instructions to the Lab 6 README.
- **Lab 7:** Replaced the empty fuzz-test starters with Hypothesis tests and hardened the parking-time, rate-lookup, and plate-formatting functions. Added test instructions and documented the accepted input formats in the Lab 7 README.
- **Dependencies:** Added `requirements.txt` for Hypothesis, pytest, and pytest-cov.

## Lab 7 input behavior

- Parking ranges must use `HH:MM-HH:MM` on a 24-hour clock. If the exit time is earlier than the entry time, it is treated as the next day.
- Vehicle names are case-insensitive and accept surrounding whitespace; unsupported values raise `ValueError`.
- Plates must follow `LLDDLLDDDD` (two ASCII letters, two digits, two ASCII letters, four digits). Valid plates are returned uppercase with groups separated by spaces. Invalid inputs raise `ValueError`.

## Verification

| Lab | Command | Result |
|---|---|---|
| 6 | `python -m pytest --cov=parking_fee --cov-branch --cov-report=term-missing` (run from `Lab 6`) | 24 passed; 100% statement and branch coverage |
| 7 | `python -m pytest` (run from `Lab 7`) | 19 passed, including Hypothesis-generated examples |

Both suites were run using the dependencies declared in `requirements.txt`.
