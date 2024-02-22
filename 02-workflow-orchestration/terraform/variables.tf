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

