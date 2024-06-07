terraform {
  required_version = ">= 1.7.4"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.36.0"
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


provider "snowflake" {
  username = var.snowflake_username
  password = var.snowflake_password
  account  = var.snowflake_account
  role     = var.snowflake_role
  region   = var.snowflake_region
}

resource "snowflake_warehouse" "example_warehouse" {
  name            = var.warehouse_name
  comment         = " Snowflake Warehouse"
  warehouse_size  = var.warehouse_size
  auto_suspend    = 60
  auto_resume     = true
}

