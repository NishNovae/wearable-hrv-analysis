# Wearable HRV Analysis
웨어러블 센서 기반 HRV, 활동량, 수면일지 데이터를 전처리하고 분석하는 프로젝트입니다.

A data analysis project using wearable sensor data, including HRV, activity, sleep diaries, and participant surveys.

## Dataset
`Springer Nature Figshare`: [*In-situ wearable-based dataset of continuous heart rate variability monitoring accompanied by sleep diaries*](https://springernature.figshare.com/articles/dataset/In-situ_wearable-based_dataset_of_continuous_heart_rate_variability_monitoring_accompanied_by_sleep_diaries/28509740?file=52669388)
- 49 healthy adults
- Wearable sensor data collected over approx. 4 weeks
- Daily sleep diaries
- Survey data for each participant
- `userId` in the sleep diary corresponds to `deviceId` in the sensor and survey data

## Week 1
### Processing Overview
The pipeline performs the following steps:

  1. Inspect `sensor_hrv_filtered.csv`, `sleep_diary.csv`, and `survey.csv`
  2. Select columns required for analysis
  3. Convert timestamps and remove invalid records
  4. Save processed datasets in `Parquet` format to `data/processed`
  5. Aggregate activity data by hour and day
  6. Generate inspection results for processed and aggregated datasets

HR and HRV variables are preserved at the original 5-minute interval level. Activity variables are additionally aggregated into hourly and daily datasets.

### Processing Pipeline
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
└─ processed/    # Processed Parquet files

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
