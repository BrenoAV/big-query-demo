import decimal

from google.cloud import bigquery

from src.bigquery import create_bigquery_client, create_dataset, upload_df_to_bigquery
from src.data import load_data

# Constants
CSV_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
COL_NAMES = ["sepal_length", "sepal_width", "petal_length", "petal_width", "class"]
DATASET_ID = "iris_dataset"
TABLE_NAME = "iris_table"

# Global Variables
bq_client = create_bigquery_client()


def main():
    """main function"""

    # Creating the pandas DataFrame
    iris_df = load_data(csv_url=CSV_URL, col_names=COL_NAMES)
    iris_df[COL_NAMES[:-1]] = iris_df[COL_NAMES[:-1]].astype(float)
    iris_df[COL_NAMES[-1]] = iris_df[COL_NAMES[-1]].astype(str)

    # BigQuery Requeriments
    context = decimal.Context(prec=7)
    for col_name in COL_NAMES[:-1]:
        iris_df[col_name] = iris_df[col_name].apply(context.create_decimal_from_float)

    schema = [
        bigquery.SchemaField(col_name, "NUMERIC")
        if col_name != "class"
        else bigquery.SchemaField(col_name, "STRING")
        for col_name in COL_NAMES
    ]
    # Creating bigquery dataset
    dataset = create_dataset(bq_client=bq_client, dataset_id=DATASET_ID)

    # Upload the dataset into bigquery
    upload_df_to_bigquery(
        bq_client=bq_client,
        dataset=dataset,
        df=iris_df,
        table_id=TABLE_NAME,
        schema=schema,
    )


if __name__ == "__main__":
    main()
