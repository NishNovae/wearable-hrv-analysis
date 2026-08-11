# Wearable HRV Analysis

웨어러블 센서 기반 HRV, 활동량, 수면일지 데이터를 전처리하고 분석하는 프로젝트입니다.

A data analysis project using wearable sensor data, including HRV, activity, sleep diaries, and participant surveys.
<p align="left">
  <img src="./assets/pipeline_overview.svg" width="900">
</p>

## Tech Stack
Data Source
<br>
<img src="https://img.shields.io/badge/Figshare-D94A4A?style=flat-square&logoColor=white"/>
<br>
Data Processing
<br>
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/><img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white"/><img src="https://img.shields.io/badge/CSV-2E8B57?style=flat-square&logoColor=white"/><img src="https://img.shields.io/badge/Parquet-7C5C99?style=flat-square&logoColor=white"/>
<br>
Data Integration
<br>
<img src="https://img.shields.io/badge/Google%20Sheets-34A853?style=flat-square&logo=googlesheets&logoColor=white"/><img src="https://img.shields.io/badge/BigQuery-4285F4?style=flat-square&logo=googlebigquery&logoColor=white"/>
<br>
Visualization
<br>
<img src="https://img.shields.io/badge/Power%20BI-F2C811?style=flat-square&logoColor=black"/>
<br>

## Dataset
`Figshare - Springer Nature`:<br> [*In-situ wearable-based dataset of continuous heart rate variability monitoring accompanied by sleep diaries*](https://springernature.figshare.com/articles/dataset/In-situ_wearable-based_dataset_of_continuous_heart_rate_variability_monitoring_accompanied_by_sleep_diaries/28509740?file=52669388)
```text
- 49 healthy adults
- Wearable sensor data collected over approx. 4 weeks
- Daily sleep diaries
- Survey data for each participant
- `userId` in the sleep diary corresponds to `deviceId` in the sensor and survey data
```

## Data Processing
```text
1. Inspect `sensor_hrv_filtered.csv`, `sleep_diary.csv`, and `survey.csv`
2. Select columns required for analysis
3. Convert timestamps and remove invalid records
4. Save processed datasets in `Parquet` format to `data/processed`
5. Aggregate activity data by hour and day
6. Export processed datasets to CSV for external data integration
7. Generate inspection results for processed and aggregated datasets
```
```text
HR and HRV variables are preserved at the original 5-minute interval level.
Activity variables are additionally aggregated into hourly and daily datasets.
Exported CSV files are manually uploaded to Google Spreadsheets for downstream BigQuery and Power BI integration.
```

### How to run the processing pipeline
#### Git Bash / Linux
```bash
./run_pipeline.sh
```

#### Windows PowerShell
```bash
.\run_pipeline.bat
```

Both scripts execute raw data inspection, preprocessing, Parquet conversion, activity aggregation, and validation.

The Windows pipeline can also be registered with Task Scheduler:
```bash
.\register_task.bat
```

To run the registered task immediately:
```bash
schtasks /run /tn "Wearable HRV Pipeline"
```

To remove the registered task:
```bash
.\unregister_task.bat
```

## Project Structure
```text
data/
├─ raw/          # Raw dataset files
├─ processed/    # Processed Parquet files
└─ export/       # csv files to export into Google Spreadsheets

docs/            # Data inspection outputs
src/             # Preprocessing and aggregation scripts
output/          # Analysis outputs

requirements.txt
set_environment
run_pipeline.sh
run_pipeline.bat
register_task.bat
unregister_task.bat
```
