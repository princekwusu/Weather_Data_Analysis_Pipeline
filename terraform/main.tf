terraform {
  required_version = ">= 1.7.4"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
}

# Define the AWS provider
provider "aws" {
  region = var.region
}

#creating resources
resource "aws_s3_bucket" "my_bucket" {
  bucket = var.bucket_name

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_object" "folder_object" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "${var.folder_name}/"  
  acl    = "private"  
}


