"""
Date: 2023-08-28
Author: brenoAV

Summary:

data.py - module for downloading or loading csv files

This module provides a functions that allow you load a dataset using a local file or
download from a url.
"""


from typing import List

import pandas as pd


def load_data(csv_url: str, col_names: List[str]) -> pd.DataFrame:
    """Load a dataset using a url or local path

    Parameters
    ----------
    csv_url : str
        url from an internet or a local file
    col_names : List[str]
        Name of columns to be used on the loaded dataset

    Returns
    -------
    pd.DataFrame
        DataFrame loaded with the columns named by `col_names` parameter
    """
    print(f"Loading the data {csv_url}...")
    df = pd.read_csv(filepath_or_buffer=csv_url, names=col_names)
    print("Data loaded!")
    return df
