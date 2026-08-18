# random_forest.py

from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GroupShuffleSplit	
# because there are mult. entries for each deviceId
# Group split to keep each deviceId entirely in train or test.

DEBUG = True

BASE_DIR = Path(__file__).resolve().parents[2]
ML_DIR = BASE_DIR / "data" / "ml"

# === import ml_daily.parquet

ml_daily = pd.read_parquet(
	ML_DIR / "ml_daily.parquet"
)

#if DEBUG:
#	print(ml_daily.columns)

# === Random Forest trial 1 -> failed

'''TARGET = "rmssd_mean"

FEATURES = [
	"sleep_duration", "sleep_latency", "sleep_efficiency",
	"steps_sum",
	"age",
	"ISI_1",	# Insomnia Severity Index 0 (none) to 28 (severe)
	"MEQ"		# morning-evening type 70 (morning) to 16 (evening)
]'''

# === Within-participant centered RF

# “RMSSD의 일별 변동이 수면시간, 수면효율, 수면잠복기, 활동량의 일별 변동과 일반적으로 어떤 관계를 갖는가?”

RAW_FEATURES = [
	"sleep_duration",
	"sleep_latency",
	"sleep_efficiency",
	"steps_sum",
]

rf_data = ml_daily[
	["deviceId", "rmssd_mean"] + RAW_FEATURES
].dropna().copy()

CENTER_COLS = ["rmssd_mean"] + RAW_FEATURES

for col in CENTER_COLS:
	rf_data[f"{col}_centered"] = (
		rf_data[col]
		- rf_data.groupby("deviceId")[col].transform("mean")
	)

TARGET = "rmssd_mean_centered"

FEATURES = [
	"sleep_duration_centered",
	"sleep_latency_centered",
	"sleep_efficiency_centered",
	"steps_sum_centered",
]

X = rf_data[FEATURES]
y = rf_data[TARGET]
groups = rf_data["deviceId"]

#if DEBUG:
#	print(rf_data.shape)
#	print(rf_data.isna().sum())
#	print(f"participants: {rf_data['deviceId'].nunique()}")

# === GroupShuffleSplit

gss = GroupShuffleSplit(
	n_splits=1,			# TBD
	train_size=0.8,		# 80% goes to train
	random_state=42,	# basically RNG seed; also good number
)

train_idx, test_idx = next(
	gss.split(X, y, groups=groups)
)

X_train = X.iloc[train_idx]
X_test = X.iloc[test_idx]

y_train = y.iloc[train_idx]
y_test = y.iloc[test_idx]

groups_train = groups.iloc[train_idx]
groups_test = groups.iloc[test_idx]

if DEBUG:
    print(f"train: {X_train.shape}")
    print(f"test: {X_test.shape}")
    print(f"train participants: {groups_train.nunique()}")
    print(f"test participants: {groups_test.nunique()}")
    print(
        "participant overlap:",
        set(groups_train) & set(groups_test)
    )

# === RandomForestRegressor

rf = RandomForestRegressor(
	n_estimators=200,
	max_depth=3,
	min_samples_leaf=10,
	random_state=42,
	n_jobs=-1,
	#min_samples_split
	#max_features
)

rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

# === RF Test

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

y_train_pred = rf.predict(X_train)

train_mae = mean_absolute_error(y_train, y_train_pred)
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
train_r2 = r2_score(y_train, y_train_pred)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"Train MAE:  {train_mae:.4f}")
print(f"Train RMSE: {train_rmse:.4f}")
print(f"Train R2:   {train_r2:.4f}")

print(f"Test MAE:   {mae:.4f}")
print(f"Test RMSE:  {rmse:.4f}")
print(f"Test R2:    {r2:.4f}")