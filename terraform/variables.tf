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
