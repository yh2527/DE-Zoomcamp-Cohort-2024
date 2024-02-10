# generate ssh keys
resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}
output "private_ssh_key" {
  value     = tls_private_key.ssh_key.private_key_pem
  sensitive = true
}
resource "local_file" "private_key_file" {
  content  = tls_private_key.ssh_key.private_key_pem
  filename = "../ssh/ssh_private_key.pem"
  file_permission = "0600"
}

# enable Compute Engine API
resource "google_project_service" "compute" {
  project                    = var.project_id
  service                    = "compute.googleapis.com"
  disable_on_destroy         = true
  disable_dependent_services = true
}

# setup VPC
resource "google_compute_network" "vpc_network" {
  project = var.project_id
  name    = var.vpc_network_name
}

# setup GCE
resource "google_compute_instance" "default" {
  project                   = var.project_id
  zone                      = var.zone
  name                      = var.gce_name
  machine_type              = "e2-standard-4"
  allow_stopping_for_update = true

  boot_disk {
    initialize_params {
      image = "ubuntu-2004-focal-v20230302"
      size  = "30"
    }
  }
  
  network_interface {
    # network = google_compute_network.vpc_network.name
    network = "default"

    access_config {
    }
  }

  metadata = {
    ssh-keys = "user1:${tls_private_key.ssh_key.public_key_openssh}"
  }

  service_account {
    scopes = ["cloud-platform"]
    email  = google_service_account.service_account.email
  }
}
