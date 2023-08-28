# -*- coding: utf-8 -*-
"""
Date: 2023-08-28
Author: brenoAV

Summary:

bigquery.py - module that allows connect with BigQuery Client (API) and execute
save/load of tables in BigQuery
"""
from typing import List, Optional

import pandas as pd
from google.cloud import bigquery
from google.cloud.exceptions import Conflict


def create_bigquery_client(credentials: Optional[str] = None) -> bigquery.Client:
    """Create a BigQuery Client using Credentials or by default using the
    env variable: GOOGLE_APPLICATION_CREDENTIALS

    Parameters
    ----------
    credentials : Optional[str]
        Credentials path with the Service Manager Authentication. If you don't provide
        will be used the system env variable: GOOGLE_APPLICATION_CREDENTIALS.

    Returns
    -------
    bigquery.Client
        A BigQuery Client instance
    """
    if credentials:
        return bigquery.Client.from_service_account_json(credentials)
    return bigquery.Client()


def create_dataset(bq_client: bigquery.Client, dataset_id: str) -> bigquery.Dataset:
    """Create a dataset in the Big Query Client and return the dataset created. If the
    dataset already exists then return the dataset

    Parameters
    ----------
    bq_client : bigquery.Client
        Big Query Client object where the dataset will be created
    dataset_id : str
        Dataset ID to be created

    Returns
    -------
    bigquery.Dataset
        Big Query Dataset object specified by the dataset_id
    """
    try:
        dataset = bq_client.create_dataset(dataset=dataset_id)
        print(f"The dataset {dataset_id} created!")
        return dataset
    except Conflict:
        print(f"The dataset {dataset_id} already exists!")
        return bq_client.get_dataset(dataset_ref=dataset_id)


def upload_df_to_bigquery(
    bq_client: bigquery.Client,
    dataset: bigquery.Dataset,
    df: pd.DataFrame,
    table_id: str,
    schema: List[bigquery.SchemaField],
) -> None:
    """Upload a Pandas DataFrame inside of BigQuery

    Parameters
    ----------
    bq_client : bigquery.Client
        Big Query Client object that will be created or updated the table
    dataset : bigquery.Dataset
        Big Query Dataset object that will be created or updated the table
    df : pd.DataFrame
        Pandas DataFrame that will recorded
    table_id : str
        Table ID to be created or udpated
    schema : List[bigquery.SchemaField]
        A list of bigquery.SchemaField specifying the type of each column of `df`
    """
    dataset_full_id = "{}.{}".format(dataset.project, dataset.dataset_id)
    destination_full = "{}.{}".format(dataset_full_id, table_id)
    job_config = bigquery.LoadJobConfig(schema=schema)
    job = bq_client.load_table_from_dataframe(
        dataframe=df, destination=destination_full, job_config=job_config
    )
    job.result()
    print(f"Saved the Dataframe inside of {destination_full}")
