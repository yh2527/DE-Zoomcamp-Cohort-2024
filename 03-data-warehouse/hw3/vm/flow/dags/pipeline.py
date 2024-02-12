from airflow.decorators import dag, task
import pendulum
from google.cloud import storage
from google.oauth2.service_account import Credentials
import pandas as pd
import os
import io
import pyarrow as pa
import pyarrow.parquet as pq

url_prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data'

@dag(
    schedule=None,
    #schedule_interval='0 5 * * *',  # daily at 05:00 UTC
    start_date=pendulum.datetime(2024, 2, 9, tz="UTC"),
    is_paused_upon_creation=False,
    catchup=False,
    tags=["hw3"],
    params={
        "color": "green",
        "year": 2022,
        "month": 1,
    },
)
def green_taxi_ingestion():

    @task()
    def df_read(url_prefix, **kwargs):
        params = kwargs['params']
        color = params['color']
        year = params['year']
        month = params['month']

        file_name = f'{url_prefix}/{color}_tripdata_{year}-{str(month).zfill(2)}.parquet'
        print(file_name)
        return pd.read_parquet(file_name)

    @task()
    def transformation(df):
        #df = df[(df['passenger_count'] > 0) & (df['trip_distance'] > 0)]
        df['lpep_pickup_date'] = df['lpep_pickup_datetime'].dt.date
        df['lpep_pickup_month'] = df['lpep_pickup_datetime'].dt.month
        def camel_to_snake(name):
            import re
            name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

        original_columns = df.columns
        df.columns = [camel_to_snake(column) for column in df.columns]
        df.reset_index(drop=True, inplace=True)
        changed_columns_count = sum(1 for original, new in zip(original_columns, df.columns) if original != new)
        
        print(f"Columns converted to snake_case: {changed_columns_count}")
        
        return df

    @task()
    def test_output(output_df):
        assert 'vendor_id' in output_df.columns, "vendor_id is not a column in the DataFrame"
        #assert (output_df['passenger_count'] > 0).all(), "Found rows with passenger_count <= 0"
        #assert (output_df['trip_distance'] > 0).all(), "Found rows with trip_distance <= 0"
        return output_df

    @task
    def upload_to_gcs(df: pd.DataFrame, bucket_name: str, **kwargs):
        params = kwargs['params']
        color = params['color']
        year = params['year']
        month = params['month']

        file_path = f'{color}/{color}_tripdata_{year}_{str(month).zfill(2)}.parquet'

        buffer = io.BytesIO()
        table = pa.Table.from_pandas(df)
        pq.write_table(table, buffer)

        client = storage.Client()
        bucket = client.bucket(bucket_name)
        """
        blobs = client.list_blobs(bucket)
        for blob in blobs:
            blob.delete()
        """
        blob = bucket.blob(file_path)
        if blob.exists():
            raise ValueError(f'File already exists in gs://{bucket_name}/{file_path}')

        buffer.seek(0)  # Go to the start of the BytesIO buffer before reading
        blob.upload_from_file(buffer, content_type='application/octet-stream')

        print(f'File uploaded to gs://{bucket_name}/{file_path}')

        return

    df = df_read(url_prefix)
    df_transformed = transformation(df)
    tested_df = test_output(df_transformed)
    upload_to_gcs(tested_df, 'hw2-storage-bucket_github-activities-412623')

green_taxi_ingestion()
