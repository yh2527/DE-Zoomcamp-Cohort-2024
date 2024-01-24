import pandas as pd
import os
from time import time
from sqlalchemy import create_engine
import argparse

### The bash command to run this pipeline that's packaged in docker: 
'''
docker run -it --network=2_docker_sql_default hw1-taxi-ingest:v001 --user p1user --password root --host pgdatabase --port 5432 --db ny_taxi --color green --year 2019 --month 09 --url https://github.com/DataTalksClub/nyc-tlc-data/releases/download/
'''

chunk_size = 100000

def ingest_tripdata(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    color = params.color
    year = params.year
    month = params.month
    url = params.url

    # Download the file using wget
    exit_code = os.system(f"wget {url}{color}/{color}_tripdata_{year}-{month}.csv.gz")

    if exit_code == 0:
        print("Download successful.")
    else:
        print("Download failed. Exit code:", exit_code)

    # Read the data into a iterator because we would like to ingest the file in smaller chunks
    df_iter = pd.read_csv(f'{color}_tripdata_{year}-{month}.csv.gz', iterator=True, chunksize=chunk_size)

    # Connect to PostgreSQL
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()
    
    # First chunk to ingest
    df0 = next(df_iter)

    # Transform two datetime columns from TEXT type
    df0.lpep_pickup_datetime = pd.to_datetime(df0.lpep_pickup_datetime)
    df0.lpep_dropoff_datetime = pd.to_datetime(df0.lpep_dropoff_datetime)
    
    # Establish the new table and schema
    df0.head(n=0).to_sql(name=f'{color}_tripdata_{year}_{month}', con=engine, if_exists='replace')
    # Ingest the first chunk
    t_start = time()
    df0.to_sql(name=f'{color}_tripdata_{year}_{month}', con=engine, if_exists='append')
    t_end = time()
    print('inserted another chunk, took %.3f second' % (t_end - t_start))
    

    # Ingest the rest of the file
    while True: 
        try:
            t_start = time()

            df = next(df_iter)

            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

            df.to_sql(name=f'{color}_tripdata_{year}_{month}', con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk, took %.3f second' % (t_end - t_start))
        
        except StopIteration:
                print("Finished ingesting data into the postgres database")
                break


def ingest_zone_code(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    color = params.color
    year = params.year
    month = params.month
    url = params.url

    # Download the file using wget
    exit_code = os.system("wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv")

    if exit_code == 0:
        print("Download successful.")
    else:
        print("Download failed. Exit code:", exit_code)

    # Read the data from a csv file
    zone = pd.read_csv('taxi+_zone_lookup.csv')

    # Connect to PostgreSQL
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()
    
    # Ingest the file
    try: 
        t_start = time()
        zone.to_sql(name='taxi_zone_lookup', con=engine, if_exists='replace')
        t_end = time()
        print('inserted another chunk, took %.3f second' % (t_end - t_start))
    except StopIteration:
        print("Finished ingesting data into the postgres database")
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--color', required=True, help='yellow or green tripdata for the table where we will write the results to')
    parser.add_argument('--year', required=True, help='year of the table where we will write the results to')
    parser.add_argument('--month', required=True, help='month of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    ingest_tripdata(args)
    ingest_zone_code(args)
