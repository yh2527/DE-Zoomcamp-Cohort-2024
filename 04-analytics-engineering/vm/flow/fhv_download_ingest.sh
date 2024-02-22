#!/bin/bash

mkdir /tmp/fhv_data/
cd /tmp/fhv_data

#URL='https://d37ci6vzurychx.cloudfront.net/trip-data/'
URL='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/'

for MONTH in {1..12}
do
    #wget "${URL}fhv_tripdata_2019-$(printf "%02d" $MONTH).parquet"
    wget "${URL}fhv_tripdata_2019-$(printf "%02d" $MONTH).csv.gz"
    sleep 30
done

# empty the destination folder in the bucket
gsutil -m rm -r gs://hw4-storage-bucket_github-activities-412623/fhv/
# ingest files from directories on vm to gcs bucket
gsutil -m cp -r /tmp/fhv_data/fhv_tripdata* gs://hw4-storage-bucket_github-activities-412623/fhv/

cd /tmp

# generate a def file in json for creating an external BigQuery table based off the data in the gcs
# if data files in the bucket are in csv, need to complete schema info in the def file
# if data files in the bucket are in csv, set "skipLeadingRows": 1 in the be_def json file
bq mkdef --source_format=CSV gs://hw4-storage-bucket_github-activities-412623/fhv/* >> fhv_bq_def
#bq mkdef --source_format=PARQUET gs://hw4-storage-bucket_github-activities-412623/fhv/* >> fhv_bq_def

# remove the target external table in BigQuery if already exists
bq rm -f -t github-activities-412623:green_tripdata.fhv_external
bq mk --table --external_table_definition=fhv_bq_def green_tripdata.fhv_external

