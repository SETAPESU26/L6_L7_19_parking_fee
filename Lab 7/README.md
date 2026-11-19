# L6_L7_19_parking_fee — Parking Fee

Lab 7: Fuzz Testing

## Tests

Install the repository test dependencies from the repository root, then run:

```sh
python -m pip install -r requirements.txt
python -m pytest
```

The Hypothesis tests generate valid parking-time ranges and license plates, and exercise invalid inputs. Parking times use a 24-hour clock; an exit time earlier than the entry time is treated as the following day. Plates use the `LLDDLLDDDD` layout (two letters, two digits, two letters, four digits).
