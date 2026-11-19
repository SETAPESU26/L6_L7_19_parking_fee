# Parking Fee Labs Report

**Name:** Armaan Ali  
**SRN:** PES2UG24CS083  
**Repository:** [L6_L7_19_parking_fee](https://github.com/SETAPESU26/L6_L7_19_parking_fee)

## Lab 6 — Code and Branch Coverage

The Lab 6 test suite exercises vehicle-specific hourly fees, free-stay and hour-rounding boundaries, EV discounts, lost-ticket fees, slot assignment, monthly-pass pricing and resident discounts, and invalid inputs. Branch coverage is enabled in the documented pytest command.

**Result:** 24 tests passed with 100% statement and branch coverage.

## Lab 7 — Fuzz Testing

Hypothesis tests generate valid and invalid inputs for all three functions. The implementation now validates malformed input and raises `ValueError` rather than failing with incidental parsing, indexing, or lookup errors.

- **`minutes_parked`:** Accepts `HH:MM-HH:MM` on a 24-hour clock. Generated time pairs check the duration modulo one day; an earlier exit time is interpreted as the next day. Invalid formats and out-of-range times are rejected.
- **`hourly_rate`:** Accepts bike, car, and truck names case-insensitively, with surrounding whitespace. Unsupported names and non-string values are rejected.
- **`format_plate`:** Accepts two ASCII letters, two digits, two ASCII letters, and four digits (`LLDDLLDDDD`). It returns uppercase groups separated by spaces and rejects malformed plates.

**Result:** 19 tests passed, including Hypothesis-generated examples.

## Dependencies and run commands

Install the requirements from the repository root with `python -m pip install -r requirements.txt`.

Run the relevant test command from each lab directory:

| Lab | Command | Result |
|---|---|---|
| 6 | `python -m pytest --cov=parking_fee --cov-branch --cov-report=term-missing` (run from `Lab 6`) | 24 passed; 100% statement and branch coverage |
| 7 | `python -m pytest` (run from `Lab 7`) | 19 passed, including Hypothesis-generated examples |

