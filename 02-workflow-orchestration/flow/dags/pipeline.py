from airflow.decorators import dag, task
import pendulum
from google.cloud import storage
from google.oauth2.service_account import Credentials
import pandas as pd
import os
import pyarrow as pa
import pyarrow.parquet as pq

url_prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
color = 'green'
years = [2020]
months = [10, 11, 12]
path_key_file = '/opt/airflow/config/sa_private_key_decoded.json'

@dag(
    schedule=None,
    #schedule_interval='0 5 * * *',  # daily at 05:00 UTC
    start_date=pendulum.datetime(2024, 2, 3, tz="UTC"),
    catchup=False,
    tags=["hw2"],
)
def green_taxi_ingestion():

    def load_data_from_api(file_url):
        taxi_dtypes = {
                        'VendorID': pd.Int64Dtype(),
                        'store_and_fwd_flag':str,
                        'RatecodeID':pd.Int64Dtype(),              
                        'PULocationID':pd.Int64Dtype(),
                        'DOLocationID':pd.Int64Dtype(),
                        'passenger_count': pd.Int64Dtype(),
                        'trip_distance': float,
                        'fare_amount': float,
                        'extra':float,
                        'mta_tax':float,
                        'tip_amount':float,
                        'tolls_amount':float,
                        'ehail_fee':float,
                        'improvement_surcharge':float,
                        'total_amount':float,
                        'payment_type': pd.Int64Dtype(),
                        'congestion_surcharge':float,
                    }
        parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']
        
        return pd.read_csv(
            file_url, sep=',', compression='gzip', dtype=taxi_dtypes, parse_dates=parse_dates
            )

    @task()
    def df_all(url_prefix, color, years, months):
        frames = []
        for y in years:
            for m in months:
                file_name = f'{url_prefix}/{color}/{color}_tripdata_{y}-{str(m).zfill(2)}.csv.gz'
                print(file_name)
                frames.append(load_data_from_api(file_name))
        return pd.concat(frames, ignore_index=True)

    @task()
    def transformation(df):
        df = df[(df['passenger_count'] > 0) & (df['trip_distance'] > 0)]
        df['lpep_pickup_date'] = df['lpep_pickup_datetime'].dt.date
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
        assert (output_df['passenger_count'] > 0).all(), "Found rows with passenger_count <= 0"
        assert (output_df['trip_distance'] > 0).all(), "Found rows with trip_distance <= 0"
        return output_df

    @task
    def upload_to_gcs(df: pd.DataFrame, bucket_name: str, table_name: str):
        project_id = 'github-activities-412623'
        root_path = f'{bucket_name}/{table_name}'
        credentials_path = os.path.expanduser(path_key_file)


        # delete existing blobs/objects
        credentials = Credentials.from_service_account_file(credentials_path)
        client = storage.Client(credentials=credentials, project=credentials.project_id)
        bucket = client.bucket(bucket_name)

        blobs = client.list_blobs(bucket, prefix=table_name)

        for blob in blobs:
            blob.delete()
        

        # ingest data into gcs
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

        table = pa.Table.from_pandas(df)
        gcs = pa.fs.GcsFileSystem()
        pq.write_to_dataset(
            table,
            root_path = root_path,
            partition_cols = ['lpep_pickup_date'],
            filesystem = gcs
        )

        # Save DataFrame to a file
        #filename = '/tmp/dataframe_to_upload.parquet'
        #df.to_parquet(filename)

        # Upload the file to GCS
        #bucket = client.bucket(bucket_name)
        #blob = bucket.blob(object_name)
        #blob.upload_from_filename(filename)

        # Optionally, remove the file after uploading
        #os.remove(filename)

        return table_name

    df = df_all(url_prefix, color, years, months)
    df_transformed = transformation(df)
    tested_df = test_output(df_transformed)
    upload_to_gcs(tested_df, 'hw2-storage-bucket_github-activities-412623',
                  'hw2_green_taxi_files')

green_taxi_ingestion()
