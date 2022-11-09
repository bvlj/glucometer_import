#!/usr/bin/env python3

from database_utils import write_to_db
from fetch_readings import fetch_readings

import sys

if __name__ == "__main__":
    args = sys.argv[1:]
    driver_name = args[0]
    db_path = args[1]
    if len(args) > 2:
        csv_path = args[2]
    else:
        csv_path = None

    df = fetch_readings(driver_name, csv_path=csv_path, verbose=True)
    write_to_db(db_path, df)
    print(f'Saved readings in {db_path}')
    print(df)
