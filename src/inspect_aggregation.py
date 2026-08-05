# inspect_aggregation.py

from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"


hourly_activity = pd.read_parquet(
    PROCESSED_DIR / "hourly_activity.parquet"
)

daily_activity = pd.read_parquet(
    PROCESSED_DIR / "daily_activity.parquet"
)


print("=== Hourly Activity ===")
print(hourly_activity.shape)
print(hourly_activity.dtypes)
print(hourly_activity.head())

print("\nsteps coverage")
print(hourly_activity["steps_coverage"].describe())

print("\nmissing steps_sum")
print(hourly_activity["steps_sum"].isna().sum())


print("\n=== Daily Activity ===")
print(daily_activity.shape)
print(daily_activity.dtypes)
print(daily_activity.head())

print("\nsteps coverage")
print(daily_activity["steps_coverage"].describe())

print("\nmissing steps_sum")
print(daily_activity["steps_sum"].isna().sum())


print("\n=== Validation ===")
print(
    "hourly coverage outside 0~1:",
    (~hourly_activity["steps_coverage"].between(0, 1)).sum(),
)

print(
    "daily coverage outside 0~1:",
    (~daily_activity["steps_coverage"].between(0, 1)).sum(),
)
