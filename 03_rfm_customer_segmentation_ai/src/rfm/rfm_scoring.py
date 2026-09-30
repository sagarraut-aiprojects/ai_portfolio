import pandas as pd


def calculate_rfm_scores(rfm):
    """
    Assign 1-5 scores to Recency, Frequency, and Monetary.

    Recency:
        Lower values receive higher scores.

    Frequency:
        Higher values receive higher scores.

    Monetary:
        Higher values receive higher scores.

    Parameters
    ----------
    rfm : pandas.DataFrame
        Customer-level RFM data.

    Returns
    -------
    pandas.DataFrame
        RFM data with scoring columns.
    """

    scored = rfm.copy()

    scored["RecencyScore"] = pd.qcut(
        scored["Recency"],
        5,
        labels=[5, 4, 3, 2, 1],
        duplicates="drop",
    )

    scored["FrequencyScore"] = pd.qcut(
        scored["Frequency"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
    )

    scored["MonetaryScore"] = pd.qcut(
        scored["Monetary"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
    )

    return scored


def assign_rfm_segments(scored_rfm):
    """
    Assign customer segments based on total RFM score.

    Parameters
    ----------
    scored_rfm : pandas.DataFrame
        RFM data containing R, F, and M scores.

    Returns
    -------
    pandas.DataFrame
        RFM data with total score and segment.
    """

    segmented = scored_rfm.copy()

    segmented["RFMScore"] = (
        segmented["RecencyScore"].astype(int)
        + segmented["FrequencyScore"].astype(int)
        + segmented["MonetaryScore"].astype(int)
    )

    segmented["Segment"] = pd.cut(
        segmented["RFMScore"],
        bins=[2, 6, 9, 12, 15],
        labels=[
            "Lost Customers",
            "At Risk",
            "Potential Customers",
            "Loyal Customers",
        ],
    )

    # Convert from categorical to regular object column
    # so that we can assign the "Champions" label.
    segmented["Segment"] = segmented["Segment"].astype(object)

    # Customers with the highest RFM scores
    segmented.loc[
        segmented["RFMScore"] >= 13,
        "Segment"
    ] = "Champions"

    return segmented