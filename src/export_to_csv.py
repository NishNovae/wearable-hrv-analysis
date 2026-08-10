# export_to_csv.py
# data/processed -> .csv -> Google Spreadsheet

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
EXPORT_DIR = BASE_DIR / "data" / "export"

EXPORT_DIR.mkdir(parents=True, exist_ok=True)

for parquet_file in PROCESSED_DIR.glob("*.parquet"):
    df = pd.read_parquet(parquet_file)

    csv_file = EXPORT_DIR / f"{parquet_file.stem}.csv"
    df.to_csv(csv_file, index=False)

    print(f"[INFO] Exported: {csv_file.name}")
