# ----------------------------------------------------------
# 1. Artifact Bucket for Pipelines, Models, Metrics
# ----------------------------------------------------------
resource "google_storage_bucket" "mlops_bucket" {
  name          = var.bucket_name
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 90
    }
  }
}

# ----------------------------------------------------------
# 2. Artifact Registry for Training Docker Images
# ----------------------------------------------------------
resource "google_artifact_registry_repository" "mlops_repo" {
  provider      = google
  repository_id = var.repo_name
  description   = "Docker repository for Vertex AI training images"
  format        = "DOCKER"
  location      = var.region
}

# ----------------------------------------------------------
# 3. Service Account for Vertex Pipelines & GitHub Actions
# ----------------------------------------------------------
resource "google_service_account" "mlops_sa" {
  account_id   = var.service_account
  display_name = "Vertex AI MLOps Service Account"
}

# ----------------------------------------------------------
# 4. IAM Roles for Service Account
# ----------------------------------------------------------
locals {
  sa_roles = [
    "roles/aiplatform.admin",
    "roles/storage.admin",
    "roles/storage.objectAdmin",
    "roles/artifactregistry.admin",
    "roles/iam.serviceAccountUser"
  ]
}

resource "google_project_iam_member" "mlops_sa_roles" {
  for_each = toset(local.sa_roles)

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.mlops_sa.email}"
}

# ----------------------------------------------------------
# 5. Vertex AI Endpoint (Optional - used for auto-deploy)
# ----------------------------------------------------------
resource "google_vertex_ai_endpoint" "mlops_endpoint" {
  display_name = "iris-classification-endpoint"
  location     = var.region
  region       = var.region
  name         = "iris-classification-endpoint"
}

