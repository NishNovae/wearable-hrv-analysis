# inspect_parquet.py

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

sensor_check = pd.read_parquet(
    PROCESSED_DIR / "sensor_5min.parquet"
)

print(sensor_check.shape)
print(sensor_check.dtypes)
print(sensor_check.head())
