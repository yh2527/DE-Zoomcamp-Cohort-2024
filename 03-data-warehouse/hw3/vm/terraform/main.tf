terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.5.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 3.0"
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
