# random_forest_5min.py

from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

DEBUG = True

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"

sensor_5min = pd.read_csv(
    RAW_DIR / "sensor_hrv_filtered.csv"
)

TARGET = "rmssd"

# Experiment A:
# non-HRV signals only
FEATURES_A = [
    "HR",
    "acc_x_avg",
    "acc_y_avg",
    "acc_z_avg",
    "light_avg",
]

# Experiment B:
# add HRV-related features
FEATURES_B = [
    "HR",
    "acc_x_avg",
    "acc_y_avg",
    "acc_z_avg",
    "light_avg",
    #"sdnn",
    #"sdsd",
    #"pnn20",
    #"pnn50",
    "lf",
    "hf",
]

FLOAT32_MAX = np.finfo(np.float32).max


def run_rf_experiment(name, features):
    rf_data = sensor_5min[
        ["deviceId"] + features + [TARGET]
    ].dropna().copy()

    # Remove values that cannot be represented safely as float32.
    # In this dataset, extreme LF/HF power values can exceed this range.
    for col in ["lf", "hf"]:
        if col in rf_data.columns:
            rf_data = rf_data[
                rf_data[col].abs() <= FLOAT32_MAX
            ]

    X = rf_data[features]
    y = rf_data[TARGET]
    groups = rf_data["deviceId"]

    if DEBUG:
        print()
        print(f"=== {name} ===")
        print(f"data shape: {rf_data.shape}")
        print(f"participants: {rf_data['deviceId'].nunique()}")

    # Keep each participant entirely in either train or test.
    gss = GroupShuffleSplit(
        n_splits=1,
        train_size=0.8,
        random_state=42,
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

        print("\nFeature min/max:")
        print(
            X_train
            .agg(["min", "max"])
            .T
        )

        print("\nInfinity counts:")
        print(
            pd.Series({
                col: np.isinf(X_train[col]).sum()
                for col in X_train.columns
            })
        )

        print("\nToo-large-for-float32 counts:")
        print(
            pd.Series({
                col: (
                    X_train[col].abs() > FLOAT32_MAX
                ).sum()
                for col in X_train.columns
            })
        )

    rf = RandomForestRegressor(
        n_estimators=200,
        max_depth=3,
        min_samples_leaf=10,
        random_state=42,
        n_jobs=-1,
    )

    rf.fit(X_train, y_train)

    y_train_pred = rf.predict(X_train)
    y_test_pred = rf.predict(X_test)

    train_mae = mean_absolute_error(
        y_train,
        y_train_pred,
    )
    train_rmse = np.sqrt(
        mean_squared_error(
            y_train,
            y_train_pred,
        )
    )
    train_r2 = r2_score(
        y_train,
        y_train_pred,
    )

    test_mae = mean_absolute_error(
        y_test,
        y_test_pred,
    )
    test_rmse = np.sqrt(
        mean_squared_error(
            y_test,
            y_test_pred,
        )
    )
    test_r2 = r2_score(
        y_test,
        y_test_pred,
    )

    print()
    print("Metrics")
    print(f"Train MAE:  {train_mae:.4f}")
    print(f"Train RMSE: {train_rmse:.4f}")
    print(f"Train R2:   {train_r2:.4f}")

    print(f"Test MAE:   {test_mae:.4f}")
    print(f"Test RMSE:  {test_rmse:.4f}")
    print(f"Test R2:    {test_r2:.4f}")

    importance = pd.Series(
        rf.feature_importances_,
        index=features,
    ).sort_values(
        ascending=False
    )

    print()
    print("Feature importance:")
    print(importance)

    return (
        rf,
        X_train,
        X_test,
        y_train,
        y_test,
    )


# === Experiment A
rf_a, X_train_a, X_test_a, y_train_a, y_test_a = (
    run_rf_experiment(
        "Experiment A: non-HRV signals",
        FEATURES_A,
    )
)

# === Experiment B
rf_b, X_train_b, X_test_b, y_train_b, y_test_b = (
    run_rf_experiment(
        "Experiment B: HRV features added",
        FEATURES_B,
    )
)