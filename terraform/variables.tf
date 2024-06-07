variable "bucket_name" {
  description = "s3 bucket name"
  type        = string
}

variable "region" {
  description = "region "
  type        = string
  default     = "us-east-2"
}

variable "folder_name" {
  description = "folder name in s3"
  type        = string
}

variable "snowflake_username" {
  description = "The Snowflake username"
  type        = string
}

variable "snowflake_password" {
  description = "The Snowflake password"
  type        = string
}

variable "snowflake_account" {
  description = "The Snowflake account identifier"
  type        = string
}

variable "snowflake_role" {
  description = "The Snowflake role to use"
  type        = string
}

variable "snowflake_region" {
  description = "The Snowflake region"
  type        = string
}

variable "warehouse_name" {
  description = "The name of the Snowflake warehouse"
  type        = string
}

variable "warehouse_size" {
  description = "The size of the Snowflake warehouse"
  type        = string
  default     = "XSMALL"
}
