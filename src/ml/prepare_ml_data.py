# prepare_ml_data.py

from pathlib import Path
import pandas as pd

DEBUG = True

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
ML_DIR = BASE_DIR / "data" / "ml"

# read .parquet

sensor_5min = pd.read_parquet(
    PROCESSED_DIR / "sensor_5min.parquet"
)

daily_activity = pd.read_parquet(
    PROCESSED_DIR / "daily_activity.parquet"
)

sleep_diary = pd.read_parquet(
    PROCESSED_DIR / "sleep_diary.parquet"
)

survey = pd.read_parquet(
    PROCESSED_DIR / "survey.parquet"
)

# sensor_5min ==> deviceId + date / RMSSD

daily_hrv = (
    sensor_5min
    .groupby(["deviceId", "date"], as_index=False)
    .agg(
        rmssd_mean=("rmssd", "mean"),
        rmssd_median=("rmssd", "median"),
        rmssd_std=("rmssd", "std"),
        hrv_intervals=("rmssd", "count"),
    )
)

# merge daily HRV with daily activity -> deviceId + date

ml_daily = daily_hrv.merge(
    daily_activity,
    on=["deviceId", "date"],
    how="left",
    validate="one_to_one",
)

# sleep_diary ==> merge on userId == deviceId, 1:1

sleep_diary = sleep_diary.rename(
    columns={"userId": "deviceId"}
)

ml_daily = ml_daily.merge(
    sleep_diary,
    on=["deviceId", "date"],
    how="left",
    validate="one_to_one",
)

# survey ==> merge on deviceId, *:1

ml_daily = ml_daily.merge(
    survey,
    on="deviceId",
    how="left",
    validate="many_to_one"
)

# save ml_daily.parquet

ML_DIR.mkdir(parents=True, exist_ok=True)
ml_daily.to_parquet(
    ML_DIR / "ml_daily.parquet",
    index=False
)

print(f"[INFO] saved: {"data/ml/ml_daily.parquet"}")
print(f"[INFO] shape: {ml_daily.shape}")

if DEBUG:
    #print(ml_daily.dtypes)
    #print()
    #print(ml_daily.isna().sum())

    print(
        ml_daily.loc[ml_daily["rmssd_std"].isna(), "hrv_intervals"]
        .value_counts()
        .sort_index()
    )