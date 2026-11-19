# L6_L7_19_parking_fee — Parking Fee

Lab 6: Code and Branch Coverage

## About

A small Python module that works out parking fees by vehicle and duration, assigns a parking slot and prices monthly passes.

## Tests

Run the tests and measure line and branch coverage from this directory:

```sh
python -m pytest --cov=parking_fee --cov-branch --cov-report=term-missing
```

The test suite covers the fee boundaries, vehicle-specific rates, EV and lost-ticket adjustments, slot assignment, monthly-pass discounts, and invalid inputs.
