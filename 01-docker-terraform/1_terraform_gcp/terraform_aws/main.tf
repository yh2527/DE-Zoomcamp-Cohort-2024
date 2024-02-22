# This terraform script configures the AWS Provider and creates an S3 storage bucket.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-west-1"
}

# Create an S3 bucket
resource "aws_s3_bucket" "terraform_test_bucket" {
  bucket = "de-project-bucket-yh2527"
}


