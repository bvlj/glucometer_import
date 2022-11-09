#!/usr/bin/env python3
import pandas as pd

import sqlite3
import sys

_TABLE_NAME = "readings"


def write_to_db(db_path: str, df: pd.DataFrame) -> None:
    db = sqlite3.connect(db_path)
    df['timestamp'] = df['timestamp'].apply(str)
    with db:
        db.execute(f"CREATE TABLE IF NOT EXISTS {_TABLE_NAME} (" +
                   "timestamp DATE UNIQUE NOT NULL" +
                   ", value INTEGER NOT NULL" +
                   ", meal INTEGER NOT NULL DEFAULT 0" +
                   ")")
        for index, row in df.iterrows():
            try:
                c = db.cursor()
                values = [row['timestamp'], row['value'], row['meal']]
                c.execute(f"INSERT INTO {_TABLE_NAME} (" +
                          "timestamp, value, meal" +
                          ") VALUES (" +
                          "?, ?, ?" +
                          ")", values)
                db.commit()
            except sqlite3.IntegrityError as e:
                err_msg = str(e)
                if "UNIQUE" in err_msg and "timestamp" in err_msg:
                    # This is fine, we don't want to duplicate entries
                    pass
                else:
                    # Unexpected error
                    raise e


def main() -> None:
    args = sys.argv[1:]
    df = pd.read_csv(args[0])
    db_path = args[1]
    write_to_db(db_path, df)


if __name__ == "__main__":
    main()
