# preprocess.py

from pathlib import Path
import pandas as pd
from columns import SENSOR_COLUMNS, SLEEP_COLUMNS, SURVEY_COLUMNS

DEBUG = False

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# === select columns ===

sensor = pd.read_csv(
    RAW_DIR / "sensor_hrv_filtered.csv",
    usecols = SENSOR_COLUMNS,
)
# sensor = pd.read_csv(path)
# sensor = sensor[SENSOR_COLUMNS]

sleep = pd.read_csv(
    RAW_DIR / "sleep_diary.csv",
    usecols = SLEEP_COLUMNS,
)

survey = pd.read_csv(
    RAW_DIR / "survey.csv",
    usecols = SURVEY_COLUMNS
)

# === set dtypes ===

sensor["datetime"] = pd.to_datetime(
    sensor["ts_start"],
    unit="ms",
)

sensor["date"] = sensor["datetime"].dt.normalize()
sleep["date"] = pd.to_datetime(sleep["date"])


if DEBUG:
    print(sensor["datetime"].dt.year.value_counts().sort_index())

# remove single timestamp outside the study period (2021).
sensor = sensor[sensor["datetime"].dt.year == 2021].copy()


# === Save preprocessed datasets ===

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
sensor.to_parquet(
    PROCESSED_DIR / "sensor_5min.parquet",
    index=False
)

sleep.to_parquet(
    PROCESSED_DIR / "sleep_diary.parquet",
    index=False
)

survey.to_parquet(
    PROCESSED_DIR / "survey.parquet",
    index=False
)

print(f"sensor: \t{sensor.shape}")
print(f"sleep: \t\t{sleep.shape}")
print(f"survey: \t{survey.shape}")
print(f"saved to: \t{PROCESSED_DIR}")




