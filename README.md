# L6_L7_19_parking_fee

Parking fee calculator with code coverage and branch coverage testing for Lab 6 and Lab 7.

## Project overview

This repository contains a Python implementation for parking fee calculations, slot assignment, and monthly pass pricing. It also includes a set of test files for validating correctness and coverage requirements.

## Student details

- Student: Armaan Ali
- SRN: PES2UG24CS083

## Included files

- `Lab 6/parking_fee.py` — module under test
- `Lab 6/test_parking_fee.py` — starter test file
- `Lab 6/CodeCoverageTest_ArmaanAli_parking_fee.py` — code coverage tests
- `Lab 6/BranchCoverageTest_ArmaanAli_parking_fee.py` — branch coverage tests
- `Lab 6/screenshots/code_coverage.png` — code coverage terminal screenshot
- `Lab 6/screenshots/branch_coverage.png` — branch coverage terminal screenshot
- `Lab 6/screenshots/ArmaanAli_PES2UG24CS083_coverage_report.pdf` — combined PDF submission

## How to run

From the project directory:

```bash
cd "L6_L7_19_parking_fee/Lab 6"
python3 -m pytest -q CodeCoverageTest_ArmaanAli_parking_fee.py
python3 -m coverage run --branch -m pytest -q BranchCoverageTest_ArmaanAli_parking_fee.py
python3 -m coverage report -m --include='*parking_fee.py'
```

## Coverage result

The project achieved 100% code coverage and 100% branch coverage for `parking_fee.py`.
