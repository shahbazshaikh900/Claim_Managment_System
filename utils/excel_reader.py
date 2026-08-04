"""
Excel Reader Module
-------------------
This module is responsible for reading the weekly claim
report Excel file and returning it as a Pandas DataFrame.
"""

from pathlib import Path
import pandas as pd


def read_excel(file_path):
    """
    Reads the Excel file and returns a DataFrame.

    Parameters:
        file_path (str or Path): Path to the Excel file.

    Returns:
        pandas.DataFrame
    """

    try:
        df = pd.read_excel(file_path)

        print(f"✅ Excel file loaded successfully.")
        print(f"📊 Total Records: {len(df)}")

        return df

    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return None