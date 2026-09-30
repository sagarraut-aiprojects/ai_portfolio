import pandas as pd


def analyze_segments(rfm_segmented):
    """
    Calculate summary statistics for each RFM customer segment.

    Parameters
    ----------
    rfm_segmented : pandas.DataFrame
        Customer-level RFM data with segment labels.

    Returns
    -------
    pandas.DataFrame
        Segment-level summary statistics.
    """

    summary = (
        rfm_segmented
        .groupby("Segment", observed=True)
        .agg(
            Customers=("CustomerID", "count"),
            AvgRecency=("Recency", "mean"),
            AvgFrequency=("Frequency", "mean"),
            AvgMonetary=("Monetary", "mean"),
            TotalRevenue=("Monetary", "sum"),
        )
        .reset_index()
    )

    # Percentage of total customers
    summary["CustomerPercentage"] = (
        summary["Customers"]
        / summary["Customers"].sum()
        * 100
    )

    # Percentage of total revenue
    summary["RevenuePercentage"] = (
        summary["TotalRevenue"]
        / summary["TotalRevenue"].sum()
        * 100
    )

    return summary


def analyze_clusters(rfm_with_clusters):
    """
    Calculate summary statistics for each K-Means cluster.

    Parameters
    ----------
    rfm_with_clusters : pandas.DataFrame
        Customer-level RFM data containing cluster labels.

    Returns
    -------
    pandas.DataFrame
        Cluster-level summary statistics.
    """

    summary = (
        rfm_with_clusters
        .groupby("Cluster")
        .agg(
            Customers=("CustomerID", "count"),
            AvgRecency=("Recency", "mean"),
            AvgFrequency=("Frequency", "mean"),
            AvgMonetary=("Monetary", "mean"),
            TotalRevenue=("Monetary", "sum"),
        )
        .reset_index()
    )

    summary["CustomerPercentage"] = (
        summary["Customers"]
        / summary["Customers"].sum()
        * 100
    )

    summary["RevenuePercentage"] = (
        summary["TotalRevenue"]
        / summary["TotalRevenue"].sum()
        * 100
    )

    return summary

def compare_segments_and_clusters(rfm_data):
    """
    Compare rule-based RFM segments with K-Means clusters.

    Returns
    -------
    pandas.DataFrame
        Customer counts for each RFM segment and K-Means cluster.
    """

    comparison = pd.crosstab(
        rfm_data["Segment"],
        rfm_data["Cluster"],
    )

    return comparison