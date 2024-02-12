variable "project_id" {
  type        = string
  description = "The name of the project"
  default     = "github-activities-412623"
}

variable "account_id" {
  description = "account_id (source: terraform.tfvars)"
  type        = string
}

variable "region" {
  type        = string
  description = "The default compute region"
  default     = "us-west2"
}

variable "zone" {
  type        = string
  description = "The default compute zone"
  default     = "us-west2-a"
}

#gcs
variable "storage_class" {
  description = "storage_class (source: terraform.tfvars)"
  type        = string
}

#gcs
variable "data_lake_bucket" {
  description = "data_lake_bucket (source: terraform.tfvars)"
  type        = string
}

#gce
variable "gce_name" {
  description = "gce_name (source: terraform.tfvars)"
  type        = string
}

#vpc
variable "vpc_network_name" {
  description = "vpc_network_name (source: terraform.tfvars)"
  type        = string
}

#static_ip name
variable "gce_static_ip_name" {
  description = "gce_static_ip_name (source: terraform.tfvars)"
  type        = string
}

#bigQuery dataset name
variable "bq_dataset" {
  description = "bq_dataset (source: terraform.tfvars)"
  type        = string
}

#bigQuery table name
variable "table_id" {
  description = "table_id (source: terraform.tfvars)"
  type        = string
}

/*
variable "repository" {
  type        = string
  description = "The name of the Artifact Registry repository to be created"
  default     = "hw2-docker-repo"
}

variable "database_user" {
  type        = string
  description = "The username of the Postgres database."
  default     = "mageuser"
}

variable "database_password" {
  type        = string
  description = "The password of the Postgres database."
  sensitive   = true
}

variable "docker_image" {
  type        = string
  description = "The docker image to deploy to Cloud Run."
 default     = "mageai/mageai:latest"
}

variable "domain" {
  description = "Domain name to run the load balancer on. Used if `ssl` is `true`."
  type        = string
  default     = ""
}

variable "ssl" {
  description = "Run load balancer on HTTPS and provision managed certificate with provided `domain`."
  type        = bool
  default     = false
}
*/
