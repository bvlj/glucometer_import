# Glucometer readings dumper tool

Fetch glucose readings from a glucometer and save them in
a sqlite database.

## Setup

Configure device access

```bash
# Add permission to access /dev/tty0
sudo usermod -a -G dialout $(whoami)
sudo usermod -a -G tty $(whoami)

# Disable ModemManager
systemctl disable ModemManager.service
systemctl stop ModemManager.service
```

Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
./main.py $DEVICE_DRIVER readings.db readings.csv
```

Where:
- `$DEVICE_DRIVER` is the name of the [driver](./glucometerutils/drivers/) to
  be used
- `readings.db` is the output path of the sqlite database
- (Optional) `readings.csv` is the path of the DataFrame CSV

## Database

Table name: `readings`

| timestamp           | value | meal |
| :------------------ | ----: | :--: |
| 2022-03-09 22:36:37 | 130   | 2    |
| 2022-03-09 19:05:22 | 79    | 1    |
| 2022-03-09 16:13:08 | 220   | 2    |
| 2022-03-09 12:43:30 | 94    | 1    |

Where:
- `timestamp` is a `NOT NULL UNIQUE DATE` in ISO8601 (`YYYY-MM-DD HH:MM:SS.SSS`)
- `value` is a `NOT NULL INTEGER`
- `meal` is a `NOT NULL INTEGER`
    - `0`: meal relation unknown
    - `1`: before meal
    - `2`: after meal
