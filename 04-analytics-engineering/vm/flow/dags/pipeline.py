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
bucket_name = 'hw4-storage-bucket_github-activities-412623'

@dag(
    schedule=None,
    #schedule_interval='0 5 * * *',  # daily at 05:00 UTC
    start_date=pendulum.datetime(2024, 2, 9, tz="UTC"),
    is_paused_upon_creation=False,
    max_active_runs=3,
    catchup=False,
    tags=["hw4"],
    params={
        "color": "green",
        "year": 2019,
        "month": 1,
    },
)
def taxi_data_ingestion():

    @task(retries=3)
    def df_read(url_prefix, color, year, month):
        '''
        params = kwargs['params']
        color = params['color']
        year = params['year']
        month = params['month']
        '''
        file_name = f'{color}_tripdata_{year}-{str(month).zfill(2)}.parquet'
        #print(file_name)
        df = pd.read_parquet(f'{url_prefix}/{file_name}')
        
        local_file_path = f'/tmp/{file_name}'
        df.to_parquet(local_file_path)

        return local_file_path

    @task()
    def transformation(df_path: str, color, year, month):

        df = pd.read_parquet(df_path)
        #df = df[(df['passenger_count'] > 0) & (df['trip_distance'] > 0)]
        #df['lpep_pickup_date'] = df['lpep_pickup_datetime'].dt.date
        #df['lpep_pickup_month'] = df['lpep_pickup_datetime'].dt.month
        def camel_to_snake(name):
            import re
            name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

        original_columns = df.columns
        df.columns = [camel_to_snake(column) for column in df.columns]
        df.reset_index(drop=True, inplace=True)
        changed_columns_count = sum(1 for original, new in zip(original_columns, df.columns) if original != new)
        print(f"Columns converted to snake_case: {changed_columns_count}")
        
        os.remove(df_path) 
        transformed_file_path = f'/tmp/{color}_tripdata_{year}-{str(month).zfill(2)}_transformed.parquet'
        df.to_parquet(transformed_file_path)

        return transformed_file_path

    @task()
    def test_output(output_df_path: str, color, year, month):

        output_df = pd.read_parquet(output_df_path)
        assert 'vendor_id' in output_df.columns, "vendor_id is not a column in the DataFrame"
        #assert (output_df['passenger_count'] > 0).all(), "Found rows with passenger_count <= 0"
        #assert (output_df['trip_distance'] > 0).all(), "Found rows with trip_distance <= 0"
        
        os.remove(output_df_path) 
        local_file_path = f'/tmp/{color}_tripdata_{year}-{str(month).zfill(2)}_tested.parquet'
        output_df.to_parquet(local_file_path)

        return local_file_path

    @task
    def upload_to_gcs(df_path: str, bucket_name: str, color, year, month):
        #print("df_path", df_path)
        #print("os.path.exists(df_path)", os.path.exists(df_path))
        
        df = pd.read_parquet(df_path)
        
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

        buffer.seek(0)  # Go to the start of the BytesIO buffer before reading
        blob.upload_from_file(buffer, content_type='application/octet-stream')

        print(f'File uploaded to gs://{bucket_name}/{file_path}')
        os.remove(df_path) 

        return

    df_path = df_read(url_prefix, "{{ params.color }}", "{{ params.year }}", "{{ params.month }}")
    df_transformed = transformation(df_path, "{{ params.color }}", "{{ params.year }}", "{{ params.month }}")
    tested_df = test_output(df_transformed, "{{ params.color }}", "{{ params.year }}", "{{ params.month }}")
    upload_to_gcs(tested_df, bucket_name, "{{ params.color }}", "{{ params.year }}", "{{ params.month }}")

taxi_data_ingestion()
