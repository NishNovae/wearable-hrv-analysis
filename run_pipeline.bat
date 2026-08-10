@echo off

cd /d "%~dp0"

if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found.
    exit /b 1
)

call .venv\Scripts\activate.bat

echo.
python src\inspect_data.py > docs\inspect_data_output.txt
if errorlevel 1 exit /b 1
echo [INFO] Raw data inspection completed.
echo.

python src\preprocess.py
if errorlevel 1 exit /b 1

python src\inspect_parquet.py > docs\inspect_parquet_output.txt
if errorlevel 1 exit /b 1

echo [INFO] Preprocessing to .parquet completed.
echo.

python src\aggregate_daily.py
if errorlevel 1 exit /b 1

python src\inspect_aggregation.py > docs\inspect_aggregation_output.txt
if errorlevel 1 exit /b 1

echo [INFO] Hourly and daily activity aggregation completed.
echo.

python src\export_to_csv.py
if errorlevel 1 exit /b 1

echo.
echo [INFO] Pipeline completed. Processed data is in data/processed, CSV exports are in data/export, inspection results are in docs.
