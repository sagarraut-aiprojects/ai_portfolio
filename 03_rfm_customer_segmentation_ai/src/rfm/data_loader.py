import pandas as pd


def load_transaction_data(file_path):
    """
    Load transaction data based on file format.

    Supported formats:
    - Excel (.xlsx)
    - CSV (.csv)
    - Parquet (.parquet)

    Parameters
    ----------
    file_path : str
        Path to the transaction data file.

    Returns
    -------
    pandas.DataFrame
        Transaction data.
    """

    if file_path.endswith(".xlsx"):
        data = pd.read_excel(file_path)

    elif file_path.endswith(".csv"):
        data = pd.read_csv(file_path)

    elif file_path.endswith(".parquet"):
        data = pd.read_parquet(file_path)

    else:
        raise ValueError(
            "Unsupported file format. "
            "Use .xlsx, .csv, or .parquet."
        )

    return data