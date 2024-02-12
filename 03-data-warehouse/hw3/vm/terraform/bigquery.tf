resource "google_bigquery_dataset" "hw3_dataset" {
  dataset_id                 = var.bq_dataset
  project                    = var.project_id
  location                   = var.region
  delete_contents_on_destroy = true
}

resource "google_bigquery_table" "external_table" {
  dataset_id          = google_bigquery_dataset.hw3_dataset.dataset_id
  table_id            = var.table_id
  deletion_protection = false
  external_data_configuration {
    autodetect    = true
    source_uris   = ["gs://${google_storage_bucket.data-lake-bucket.name}/*"]
    source_format = "PARQUET"
  }
  depends_on = [google_compute_instance.default]
}
