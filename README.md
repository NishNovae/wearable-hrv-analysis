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


## Project Structure

```text
data/
├─ raw/
└─ processed/

docs/
└─ inspect_data_output.txt

src/
├─ columns.py
├─ inspect_data.py
└─ preprocess.py

output/
requirements.txt
set_environment
```

- `inspect_data.py` generates the initial data inspection results stored in `docs/inspect_data_output.txt`.
