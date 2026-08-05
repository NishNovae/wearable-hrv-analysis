# aggregate_daily.py

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# === Load 5-minute activity data ===

sensor = pd.read_parquet(
    PROCESSED_DIR / "sensor_5min.parquet",
    columns = ["deviceId", "datetime", "date", "steps"],
)

# === Create hourly time key ===

sensor["hour"] = sensor["datetime"].dt.floor("h")


# === Aggregate into hourly activity ===

hourly_activity = (
    sensor.groupby(
        ["deviceId", "date", "hour"],
        as_index=False,
    )
    .agg(
        steps_sum=(
            "steps", 
            lambda values: values.sum(min_count=1)
        ),
        steps_max_5min=(
            "steps", "max"
        ),
        sensor_intervals=(
            "steps", "size"
        ),
        steps_observed=(
            "steps", "count"
        ),
    )
)

hourly_activity["steps_coverage"] = (
    hourly_activity["steps_observed"]
    / hourly_activity["sensor_intervals"]
)

# === Aggregate into daily activity ===

daily_activity = (
    sensor.groupby(
        ["deviceId", "date"],
        as_index=False,
    )
    .agg(
        steps_sum=(
            "steps",
            lambda values: values.sum(min_count=1),
        ),
        steps_max_5min=(
            "steps",
            "max",
        ),
        sensor_intervals=(
            "steps",
            "size",
        ),
        steps_observed=(
            "steps",
            "count",
        ),
    )
)

daily_activity["steps_coverage"] = (
    daily_activity["steps_observed"]
    / daily_activity["sensor_intervals"]
)


# === Save aggregated datasets ===

hourly_activity.to_parquet(
    PROCESSED_DIR / "hourly_activity.parquet",
    index=False,
)

daily_activity.to_parquet(
    PROCESSED_DIR / "daily_activity.parquet",
    index=False,
)


print(f"hourly activity: {hourly_activity.shape}")
print(f"daily activity:  {daily_activity.shape}")
print(f"saved to:        {PROCESSED_DIR}")










