terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.5.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "3.1.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

resource "google_service_account" "service_account" {
  project      = var.project_id
  account_id   = var.account_id
  display_name = "Create service-account via terraform"
}

resource "google_service_account_key" "service_account_key" {
  service_account_id = google_service_account.service_account.name
}

resource "google_project_iam_binding" "service_account" {
  project = var.project_id
  for_each = toset([
    "roles/storage.admin",
    "roles/storage.objectAdmin"
  ])
  role = each.key
  members = [
    "serviceAccount:${google_service_account.service_account.email}",
  ]
}

resource "local_file" "sa_private_key_file" {
  content      = google_service_account_key.service_account_key.private_key
  filename     = "${path.module}/sa_private_key.json"
  file_permission = "0600"
}

