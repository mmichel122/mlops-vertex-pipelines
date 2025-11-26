variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "region" {
  type    = string
}

variable "bucket_name" {
  type    = string
}

variable "repo_name" {
  type    = string
}

variable "service_account" {
  type    = string
  default = "vertex-mlops-sa"
}

variable "github_repo" {
  type        = string
  description = "GitHub repo in format: org/repo"
}
