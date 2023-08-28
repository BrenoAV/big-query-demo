from google.cloud import bigquery

from src.bigquery import create_bigquery_client

# CONSTANTS

DATASET_ID = "iris_dataset"
TABLE_ID = "iris_table"

bq_client = create_bigquery_client()


def main():
    """main function"""
    dataset = bq_client.get_dataset(DATASET_ID)
    table_id_full = "{}.{}.{}".format(dataset.project, dataset.dataset_id, TABLE_ID)
    table = bq_client.get_table(table_id_full)
    print(f"table schema: {table.schema}")
    print(f"table num rows: {table.num_rows}")
    print(f"table num cols: {len(table.schema)}")


if __name__ == "__main__":
    main()
