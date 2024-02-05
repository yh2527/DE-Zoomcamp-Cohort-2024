variable "project_id" {
  type        = string
  description = "The name of the project"
  default     = "github-activities-412623"
}

variable "account_id" {
  description = "account_id (source: .env)"
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
  description = "storage_class (source: .env)"
  type        = string
}

#gcs
variable "data_lake_bucket" {
  description = "data_lake_bucket (source: .env)"
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
