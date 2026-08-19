from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"

BEST_K = 3

CLUSTER_FEATURES = [
    "HR",
    "acc_magnitude",
    "light_avg",
]

PROFILE_FEATURES = [
    "rmssd",
    "sdnn",
    "missingness_score",
]


# === Load data

sensor_5min = pd.read_csv(
    RAW_DIR / "sensor_hrv_filtered.csv"
)


# === Derived features

sensor_5min["acc_magnitude"] = np.sqrt(
    sensor_5min["acc_x_avg"] ** 2
    + sensor_5min["acc_y_avg"] ** 2
    + sensor_5min["acc_z_avg"] ** 2
)


# === Prepare clustering data

cluster_data = sensor_5min[
    ["deviceId"]
    + CLUSTER_FEATURES
    + PROFILE_FEATURES
].dropna().copy()


# === Scaling

scaler = StandardScaler()

X_scaled = scaler.fit_transform(
    cluster_data[CLUSTER_FEATURES]
)


# === K-Means clustering

kmeans = KMeans(
    n_clusters=BEST_K,
    random_state=42,
    n_init="auto",
)

cluster_data["cluster"] = kmeans.fit_predict(
    X_scaled
)


# === Cluster counts

print("\n=== Cluster counts ===")

print(
    cluster_data["cluster"]
    .value_counts()
    .sort_index()
)


# === Standardized cluster centroids

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


# === PCA

pca = PCA(
    n_components=2,
)

X_pca = pca.fit_transform(
    X_scaled
)

cluster_data["pc1"] = X_pca[:, 0]
cluster_data["pc2"] = X_pca[:, 1]


# === PCA explained variance

print(
    "\n=== PCA explained variance ==="
)

print(
    pca.explained_variance_ratio_
)

print(
    "Total:",
    pca.explained_variance_ratio_.sum(),
)


# === PCA loadings

loadings = pd.DataFrame(
    pca.components_.T,
    index=CLUSTER_FEATURES,
    columns=["PC1", "PC2"],
)

print(
    "\n=== PCA loadings ==="
)

print(loadings)


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