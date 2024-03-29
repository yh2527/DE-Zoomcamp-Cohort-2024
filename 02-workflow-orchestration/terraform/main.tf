# Terraform Configuration for GCP Resources

# This Terraform scripts defines the required providers, specifies the GCP project, region, and zone settings, 
# and manages the creation and configuration of a service account with specific roles. Additionally,
# it handles the generation and local storage of a service account key for secure access.

# Key components include:
# - Configuration of the `google` provider with project, region, and zone information
# - Creation of a Google Service Account and Service Account Key for managing GCP resources
# - Assignment of IAM roles (`storage.admin`, `storage.objectAdmin`) to the service account for GCS
# - Generation and local storage of the service account's private key in decoded format for external use

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.5.0"
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

resource "local_file" "sa_private_key_file_decoded" {
  content         = base64decode(google_service_account_key.service_account_key.private_key)
  filename        = "../flow/config/sa_private_key_decoded.json"
  file_permission = "0600"
}

