# inspect_data.py

from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")

files = [
    "sensor_hrv_filtered.csv",
    "sleep_diary.csv",
    "survey.csv",
]

for filename in files:
    path = RAW_DIR / filename
    df = pd.read_csv(path)

    print(f"\n{'=' * 60}")
    print(filename)
    print(f"shape: {df.shape}")

    print("\ncolumns:")
    print(df.columns.tolist())

    print("\ndtypes:")
    print(df.dtypes)

    print("\nfirst rows:")
    print(df.head())

    print("\nmissing values:")
    print(df.isna().sum())
