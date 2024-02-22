#!/bin/bash

DAG_ID="taxi_data_ingestion"

for COLOR in yellow green
do
    for YEAR in 2019 2020
    do
        for MONTH in {1..12}
        do
            sudo docker exec -it tmp-airflow-webserver-1 airflow dags trigger -c "{\"color\": \"${COLOR}\", \"year\":${YEAR}, \"month\":${MONTH}}" ${DAG_ID}
            
            if [ $? -eq 0 ]; then
                echo "Successfully triggered ${DAG_ID} for Year: ${YEAR}, Month: ${MONTH}"
            else
                echo "Failed to trigger ${DAG_ID} for Year: ${YEAR}, Month: ${MONTH}"
            fi
        done
    done
done
