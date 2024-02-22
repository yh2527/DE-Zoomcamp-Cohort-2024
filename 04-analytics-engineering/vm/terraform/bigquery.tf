# Terraform Configuration for BigQuery Dataset and External Tables Setup

resource "google_bigquery_dataset" "bq_dataset" {
  dataset_id                 = var.bq_dataset
  project                    = var.project_id
  location                   = var.region
  delete_contents_on_destroy = true
}

resource "google_bigquery_table" "external_table_yellow" {
  dataset_id          = google_bigquery_dataset.bq_dataset.dataset_id
  table_id            = var.table_id_yellow
  deletion_protection = false
  external_data_configuration {
    autodetect    = true
    source_uris   = ["gs://${google_storage_bucket.data-lake-bucket.name}/yellow/*"]
    source_format = "PARQUET"
  }
  depends_on = [google_compute_instance.default]
}

resource "google_bigquery_table" "external_table_green" {
  dataset_id          = google_bigquery_dataset.bq_dataset.dataset_id
  table_id            = var.table_id_green
  deletion_protection = false
  external_data_configuration {
    autodetect    = true
    source_uris   = ["gs://${google_storage_bucket.data-lake-bucket.name}/green/*"]
    source_format = "PARQUET"
  }
  depends_on = [google_compute_instance.default]
}
