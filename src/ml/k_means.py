from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

DEBUG = True

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"

sensor_5min = pd.read_csv(
    RAW_DIR / "sensor_hrv_filtered.csv"
)

# === Derived features

# Acceleration magnitude
sensor_5min["acc_magnitude"] = np.sqrt(
    sensor_5min["acc_x_avg"] ** 2
    + sensor_5min["acc_y_avg"] ** 2
    + sensor_5min["acc_z_avg"] ** 2
)

# Timestamp -> hour of day
sensor_5min["datetime"] = pd.to_datetime(
    sensor_5min["ts_start"],
    unit="ms",
)

sensor_5min["hour"] = sensor_5min["datetime"].dt.hour


# === Feature sets

# Features used to CREATE clusters
CLUSTER_FEATURES = [
    "HR",
    "acc_magnitude",
    "light_avg",
]

# Variables used only AFTER clustering
PROFILE_FEATURES = [
    "rmssd",
    "sdnn",
    "missingness_score",
]


# === Prepare clustering data

cluster_data = sensor_5min[
    [
        "deviceId",
        "hour",
    ]
    + CLUSTER_FEATURES
    + PROFILE_FEATURES
].dropna().copy()

'''if DEBUG:
    print("=== Input data ===")
    print(f"shape: {cluster_data.shape}")

    print("\nCluster feature summary:")
    print(
        cluster_data[
            CLUSTER_FEATURES
        ].describe()
    )
'''

# === Scaling

scaler = StandardScaler()

X_scaled = scaler.fit_transform(
    cluster_data[CLUSTER_FEATURES]
)


# === Compare k
'''
scores = {}

print("\n=== Silhouette scores ===")

for k in range(2, 7):
    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init="auto",
    )

    labels = model.fit_predict(
        X_scaled
    )

    score = silhouette_score(
        X_scaled,
        labels,
    )

    scores[k] = score

    print(
        f"k={k}: "
        f"silhouette={score:.4f}"
    )


# === Select best k

BEST_K = max(
    scores,
    key=scores.get,
)

print(
    f"\nBest k: {BEST_K} "
    f"(silhouette={scores[BEST_K]:.4f})"
)
'''

BEST_K = 3

# === Final K-Means model

kmeans = KMeans(
    n_clusters=BEST_K,
    random_state=42,
    n_init="auto",
)

cluster_data["cluster"] = (
    kmeans.fit_predict(
        X_scaled
    )
)


# === Cluster counts

print("\n=== Cluster counts ===")

print(
    cluster_data["cluster"]
    .value_counts()
    .sort_index()
)


# === Standardized centroids

centroids = pd.DataFrame(
    kmeans.cluster_centers_,
    columns=CLUSTER_FEATURES,
)

centroids.index.name = "cluster"

print(
    "\n=== Standardized cluster centroids ==="
)

print(centroids)


# === Cluster profiles in original units

pd.set_option(
    "display.max_columns",
    None,
)

cluster_profile = (
    cluster_data
    .groupby("cluster")[
        CLUSTER_FEATURES
        + PROFILE_FEATURES
    ]
    .mean()
)

print(
    "\n=== Cluster profile "
    "(original units) ==="
)

print(cluster_profile)


# === Cluster distribution by participant
'''
participant_cluster_ratio = pd.crosstab(
    cluster_data["deviceId"],
    cluster_data["cluster"],
    normalize="index",
)

print(
    "\n=== Cluster ratio by participant ==="
)

print(participant_cluster_ratio)

print(
    "\n=== Participant cluster ratio summary ==="
)

print(
    participant_cluster_ratio.describe()
)

'''
# === Cluster distribution by hour
'''
hour_cluster_ratio = pd.crosstab(
    cluster_data["hour"],
    cluster_data["cluster"],
    normalize="index",
)

print(
    "\n=== Cluster ratio by hour ==="
)

print(hour_cluster_ratio)


# === Observation counts by hour
# Useful for checking whether some hours have
# very little data.

hour_counts = (
    cluster_data["hour"]
    .value_counts()
    .sort_index()
)

print(
    "\n=== Observation counts by hour ==="
)

print(hour_counts)
'''

# === PCA

pca = PCA(
    n_components=2,
    random_state=42,
)

X_pca = pca.fit_transform(
    X_scaled
)

cluster_data["pc1"] = X_pca[:, 0]
cluster_data["pc2"] = X_pca[:, 1]

print(
    "\n=== PCA explained variance ratio ==="
)

print(
    pca.explained_variance_ratio_
)


# === PCA visualization

plt.figure(
    figsize=(8, 6)
)

for cluster_id in sorted(
    cluster_data["cluster"].unique()
):
    subset = cluster_data[
        cluster_data["cluster"]
        == cluster_id
    ]

    plt.scatter(
        subset["pc1"],
        subset["pc2"],
        s=8,
        alpha=0.3,
        label=f"Cluster {cluster_id}",
    )

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title(
    "K-Means Clusters in PCA Space"
)
plt.legend()

plt.tight_layout()
plt.show()

loadings = pd.DataFrame(
    pca.components_.T,
    index=CLUSTER_FEATURES,
    columns=["PC1", "PC2"],
)

print("\n=== PCA loadings ===")
print(loadings)

print("\n=== PCA explained variance ===")
print(
    pca.explained_variance_ratio_,
    pca.explained_variance_ratio_.sum(),
)

loadings = pd.DataFrame(
    pca.components_.T,
    index=CLUSTER_FEATURES,
    columns=["PC1", "PC2"],
)

print("\n=== PCA loadings ===")
print(loadings)