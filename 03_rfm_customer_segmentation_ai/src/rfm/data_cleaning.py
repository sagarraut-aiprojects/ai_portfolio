import pandas as pd


def generate_data_quality_report(data):
    """
    Generate a basic data quality report for transaction data.
    """

    report = {
        "rows": len(data),
        "columns": len(data.columns),
        "missing_values": data.isna().sum(),
        "duplicate_rows": data.duplicated().sum(),
        "negative_quantities": (data["Quantity"] < 0).sum(),
        "zero_quantities": (data["Quantity"] == 0).sum(),
        "negative_prices": (data["UnitPrice"] < 0).sum(),
        "zero_prices": (data["UnitPrice"] == 0).sum(),
        "cancelled_invoices": (
            data["InvoiceNo"].astype(str).str.startswith("C")
        ).sum(),
    }

    return report


def clean_transactions(data):
    """
    Clean transaction data for customer-level RFM analysis.

    Cleaning rules:
    1. Remove exact duplicate rows.
    2. Remove transactions without CustomerID.
    3. Remove cancelled invoices.
    4. Remove non-positive quantities.
    5. Remove non-positive UnitPrice values.

    Parameters
    ----------
    data : pandas.DataFrame
        Raw transaction data.

    Returns
    -------
    pandas.DataFrame
        Clean transaction data suitable for RFM analysis.
    """

    clean_data = data.copy()

    clean_data["StockCode"] = clean_data["StockCode"].astype(str)
    clean_data["InvoiceNo"] = clean_data["InvoiceNo"].astype(str)

    # Remove exact duplicate records
    clean_data = clean_data.drop_duplicates()

    # Customer-level RFM requires a customer identifier
    clean_data = clean_data.dropna(subset=["CustomerID"])

    # Remove cancelled invoices
    clean_data = clean_data[
        ~clean_data["InvoiceNo"].astype(str).str.startswith("C")
    ]

    # Keep only positive purchase quantities
    clean_data = clean_data[clean_data["Quantity"] > 0]

    # Keep only positive prices
    clean_data = clean_data[clean_data["UnitPrice"] > 0]

    return clean_data