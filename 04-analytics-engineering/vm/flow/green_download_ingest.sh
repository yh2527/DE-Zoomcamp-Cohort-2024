#!/bin/bash

mkdir -p /tmp/green_tripdata/
cd /tmp/green_tripdata

URL='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/'

for YEAR in 2019 2020
do
        for MONTH in {1..12}
        do
            wget "${URL}green_tripdata_${YEAR}-$(printf "%02d" $MONTH).csv.gz"
        done
done
gsutil -m cp -r /tmp/green_tripdata/green_tripdata* gs://hw4-storage-bucket_github-activities-412623/green/

cd /tmp

# generate a def file in json for creating an external BigQuery table based off the data in the gcs
# if data files in the bucket are in csv, need to complete schema info in the def file
# if data files in the bucket are in csv, set "skipLeadingRows": 1 in the be_def json file
bq mkdef --source_format=CSV gs://hw4-storage-bucket_github-activities-412623/green/* >> green_bq_def
bq mk --table --external_table_definition=green_bq_def green_tripdata.green_tripdata_external
