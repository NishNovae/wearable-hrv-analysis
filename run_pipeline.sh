#!/usr/bin/env bash

set -e

cd "$(dirname "$0")"

if [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "[ERROR] Virtual environment not found."
    exit 1
fi

echo
python src/inspect_data.py > docs/inspect_data_output.txt
echo "[INFO] raw data inspection completed."
echo

python src/preprocess.py
python src/inspect_parquet.py > docs/inspect_parquet_output.txt

echo "[INFO] preprocessing to .parquet completed."
echo

python src/aggregate_daily.py
python src/inspect_aggregation.py > docs/inspect_aggregation_output.txt

echo "[INFO] Hourly and daily activity aggregation completed."
echo

python src/export_to_csv.py

echo
echo "[INFO] Pipeline completed. Processed data is in data/processed, CSV exports are in data/export, inspection results are in docs."
