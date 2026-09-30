import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


def prepare_rfm_for_clustering(rfm):
    """
    Transform and standardize RFM variables for clustering.

    Log transformation reduces the effect of extreme values.
    Standardization puts Recency, Frequency, and Monetary
    on comparable scales.

    Parameters
    ----------
    rfm : pandas.DataFrame
        Customer-level RFM data.

    Returns
    -------
    tuple
        Transformed RFM data and fitted StandardScaler.
    """

    features = rfm[
        ["Recency", "Frequency", "Monetary"]
    ].copy()

    # Log transformation
    features_log = np.log1p(features)

    # Standardization
    scaler = StandardScaler()

    features_scaled = scaler.fit_transform(features_log)

    scaled_rfm = pd.DataFrame(
        features_scaled,
        columns=["Recency", "Frequency", "Monetary"],
        index=rfm.index,
    )

    return scaled_rfm, scaler





def evaluate_kmeans(scaled_rfm, k_range=range(2, 9)):
    """
    Evaluate K-Means clustering for different numbers of clusters.

    Uses:
    - Inertia (within-cluster sum of squares)
    - Silhouette score

    Parameters
    ----------
    scaled_rfm : pandas.DataFrame
        Standardized RFM features.
    k_range : range, optional
        Values of k to evaluate.

    Returns
    -------
    pandas.DataFrame
        Evaluation results for each k.
    """

    results = []

    for k in k_range:

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10,
        )

        labels = model.fit_predict(scaled_rfm)

        results.append(
            {
                "K": k,
                "Inertia": model.inertia_,
                "SilhouetteScore": silhouette_score(
                    scaled_rfm,
                    labels,
                ),
            }
        )

    return pd.DataFrame(results)


def perform_kmeans(scaled_rfm, n_clusters=3):
    """
    Perform K-Means clustering on standardized RFM data.

    Parameters
    ----------
    scaled_rfm : pandas.DataFrame
        Standardized RFM features.
    n_clusters : int, optional
        Number of clusters.

    Returns
    -------
    tuple
        Cluster labels and fitted KMeans model.
    """

    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10,
    )

    labels = model.fit_predict(scaled_rfm)

    return labels, model

def name_clusters(rfm_clustered):
    """
    Assign business-readable names to K-Means clusters
    based on their observed RFM profiles.
    """

    cluster_names = {
        0: "Active Growth Customers",
        1: "High-Value Loyal Customers",
        2: "Inactive Low-Value Customers",
    }

    result = rfm_clustered.copy()

    result["ClusterName"] = result["Cluster"].map(
        cluster_names
    )

    return result