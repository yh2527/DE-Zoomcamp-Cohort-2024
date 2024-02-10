#!/bin/bash

DAG_ID="green_taxi_ingestion"
YEAR=2022

for MONTH in {1..12}
do
    sudo docker exec -it user1-airflow-webserver-1 airflow dags trigger -c "{\"year\":${YEAR}, \"month\":${MONTH}}" ${DAG_ID}
    
    echo "Triggered ${DAG_ID} for Year: ${YEAR}, Month: ${MONTH}"
done

