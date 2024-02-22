# GCP Configuration Variables

# Update these variables to match your GCP Project ID, region, and zone preferences.
project_id = "github-activities-412623" # CHANGE-THIS
region     = "us-west2"        # CHANGE-THIS
zone       = "us-west2-a"      # CHANGE-THIS

# Additional Configuration
account_id         = "hw4-zoomcamp-account"
#vpc_network_name   = "vm-vpc-hw4"
gce_name           = "vm-hw4"
gce_static_ip_name = "static-hw4-pipeline"
storage_class      = "STANDARD"
data_lake_bucket   = "hw4-storage-bucket"
bq_dataset         = "green_tripdata"
table_id_yellow    = "yellow_tripdata_external"
table_id_green     = "green_tripdata_external"
