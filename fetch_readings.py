#!/usr/bin/env python3
import sys

from glucometerutils import driver
from glucometerutils.common import GlucoseReading, Meal
from pandas import DataFrame
from utils import print_inline
from typing import Optional

_DF_COLUMNS = ["timestamp", "value", "meal"]


def _meal_to_int(meal_value: Meal):
    if meal_value == Meal.BEFORE:
        return 1
    elif meal_value == Meal.AFTER:
        return 2
    else:
        return 0


def fetch_readings(driver_name: str,
                   csv_path: Optional[str] = None,
                   verbose: bool = True) -> DataFrame:
    if verbose:
        print(f'Importing readings from {driver_name} device...')
    requested_driver = driver.load_driver(driver_name)

    device = requested_driver.device(None)
    device.connect()

    num_readings = device.get_reading_count()
    i = 1
    def process_reading(r: GlucoseReading) -> GlucoseReading:
        nonlocal i
        if verbose:
            print_inline(f'{i}/{num_readings}: {r.timestamp}')
            i += 1
        return r


    readings = [process_reading(r) for r in device.get_readings()]
    reading_rows = []
    for r in sorted(readings, key=lambda x: x.timestamp):
        reading_rows.append([r.timestamp, r.value, _meal_to_int(r.meal)])

    print_inline(f'Imported {i} readings')

    df = DataFrame(columns=_DF_COLUMNS, data=reading_rows)
    if csv_path is not None:
        if verbose:
            print(f'Exported readings to {csv_path}')
        df.to_csv(csv_path, index=False)

    return df


def main():
    args = sys.argv[1:]
    print(fetch_readings(args[0], csv_path=args[1]))


if __name__ == "__main__":
    main()
