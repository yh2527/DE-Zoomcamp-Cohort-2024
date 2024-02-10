<h3>SQL code for HW3 BigQuery</h3>

#To create the external table containing all 2022 green tripdata:
```
CREATE EXTERNAL TABLE `github-activities-412623.hw3.green_2022_external`
OPTIONS (
    format = 'PARQUET',
    uris = ['gs://hw2-storage-bucket_github-activities-412623/green/*.parquet']
)
```
```
CREATE TABLE `github-activities-412623.hw3.green_2022_materialized`
AS
SELECT *
FROM `github-activities-412623.hw3.green_2022_external`
```
```
select count(*)
from github-activities-412623.hw3.green_2022_external
where fare_amount = 0
```
```
select count(distinct pu_location_id)
from `github-activities-412623.hw3.green_2022_materialized`
```
```
CREATE TABLE `github-activities-412623.hw3.green_2022_parition_cluster`
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY pu_location_id
AS
SELECT *
FROM `github-activities-412623.hw3.green_2022_external`
```
```
select distinct pu_location_id
from `github-activities-412623.hw3.green_2022_materialized`
where lpep_pickup_datetime between '2022-06-01' and '2022-06-30' 
```
```
select distinct pu_location_id
from `github-activities-412623.hw3.green_2022_parition_cluster`
where lpep_pickup_datetime between '2022-06-01' and '2022-06-30'
```
