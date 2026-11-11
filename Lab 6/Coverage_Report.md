# Lab 6 – Code and Branch Coverage Analysis

**Name:** Ahan A Mysore
**SRN:** PES1UG24AM019
**Module under test:** `parking_fee.py` (`parking_fee`, `find_slot`, `monthly_pass`)

## 1. Baseline (starter test file)

`test_parking_fee.py` has two tests: a free 20-minute car stay, and a car slot with 5 free slots.

| Metric | Result |
|--------|--------|
| Statements missed | 19 of 34 |
| Branches partially covered | 8 of 24 |
| Total coverage (line + branch) | 40% |

Untested: both `ValueError` checks in `parking_fee`, the hour-rounding logic, the EV discount, the lost-ticket penalty, the `full` / `ground floor` / `basement` slot outcomes, and all of `monthly_pass`.

## 2. Code (line) coverage

File: `CodeCoverageTest_parking_fee_application.py` – 13 tests.
Command: `coverage run --include=parking_fee.py -m pytest CodeCoverageTest_parking_fee_application.py` then `coverage report -m`.

| Stmts | Miss | Cover |
|-------|------|-------|
| 34 | 0 | **100%** |

Screenshot: `code_coverage.png`.

Each test targets lines no earlier test reached: unknown vehicle (line 6), negative minutes (8), 90-minute paid stay (12–15), EV car (17), lost ticket (19), each `find_slot` return (25, 27, 29) and `monthly_pass` for bike, resident car and truck (34–42).

**Limitation of line coverage.** Re-running this same file with `--branch` gives 98%, with branch `13->15` missing. No test uses an exact-hour stay (such as 60 minutes), so the "no round-up" path of `if minutes % 60 != 0` is never taken, even though every line executes. This is the false sense of security the handout describes.

## 3. Branch coverage

File: `BranchCoverageTest_parking_fee_application.py` – 30 tests.
Command: `coverage run --branch --include=parking_fee.py -m pytest BranchCoverageTest_parking_fee_application.py` then `coverage report -m`.

| Stmts | Miss | Branch | BrPart | Cover |
|-------|------|--------|--------|-------|
| 34 | 0 | 24 | 0 | **100%** |

Screenshot: `branch_coverage.png`.

Every decision is exercised as both True and False:

| Decision | True case | False case |
|----------|-----------|------------|
| `vehicle not in HOURLY_RATE` | `"cycle"` | `"bike"` |
| `minutes < 0` | -1 | 0 |
| `minutes <= 30` | 30 | 31 |
| `minutes % 60 != 0` | 61 | 60 |
| `is_ev and vehicle != "truck"` | EV car/bike | EV truck, non-EV |
| `lost_ticket` | 61 min + lost | ticket present |
| `free_slots <= 0` | 0 and -3 | 5 |
| `is_disabled` | disabled | not disabled |
| `vehicle == "truck"` (`find_slot`) | truck | car/bike |
| `vehicle == "bike"` / `"car"` (`monthly_pass`) | bike, car | truck, cycle |
| `is_resident` | resident | non-resident |

Extra edge cases: boundaries at 0, 30, 31, 60 and 61 minutes, integer division in the EV discount (`10 // 2 = 5`), EV discount applied before the lost-ticket penalty (`60 // 2 + 200 = 230`), a full lot overriding a disabled-slot request, and a disabled truck getting the ground floor rather than the basement.

## 4. Conclusion

| Stage | Line | Branch (24 branches) |
|-------|------|----------------------|
| Starter tests | 44% (15 of 34 statements) | 8 partially covered |
| Code coverage tests | 100% | 98% (`13->15` missed) |
| Branch coverage tests | 100% | 100% |

Both targets of at least 90% were met. 100% coverage shows that every line and branch was executed, not that the logic is correct. The assertions were hand-computed from the rate table and discount rules to check the outputs.
