import pandas as pd


def calculate_rfm(data):
    """
    Calculate Recency, Frequency, and Monetary value
    for each customer.

    Parameters
    ----------
    data : pandas.DataFrame
        Clean transaction data.

    Returns
    -------
    pandas.DataFrame
        Customer-level RFM table.
    """

    data = data.copy()

    # Calculate revenue for each transaction
    data["Revenue"] = data["Quantity"] * data["UnitPrice"]

    # Determine the last date in the dataset
    reference_date = data["InvoiceDate"].max()

    # Calculate RFM metrics for each customer
    rfm = data.groupby("CustomerID").agg(
        Recency=(
            "InvoiceDate",
            lambda x: (reference_date - x.max()).days
        ),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("Revenue", "sum"),
    ).reset_index()

    return rfm