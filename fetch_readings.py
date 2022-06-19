#!/usr/bin/env python3
import pandas as pd

import sys

from glucometerutils import common, driver, exceptions
from typing import Optional

_DF_COLUMNS = ["timestamp", "value", "meal"]


def _meal_to_int(meal_value: common.Meal):
    if meal_value == common.Meal.BEFORE:
        return 1
    elif meal_value == common.Meal.AFTER:
        return 2
    else:
        return 0


def fetch_readings(driver_name: str, df_path: Optional[str]) -> None:
    requested_driver = driver.load_driver(driver_name)

    device = requested_driver.device(None)
    device.connect()

    readings = device.get_readings()
    reading_rows = []
    for r in sorted(readings, key=lambda x: x.timestamp):
        reading_rows.append([r.timestamp, r.value, _meal_to_int(r.meal)])

    df = pd.DataFrame(columns=_DF_COLUMNS, data=reading_rows)
    if df_path is not None:
        df.to_csv(df_path, index=False)
    return df


def main():
    args = sys.argv[1:]
    print(fetch_readings(args[0], args[1]))


if __name__ == "__main__":
    main()
