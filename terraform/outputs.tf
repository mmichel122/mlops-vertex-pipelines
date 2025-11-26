output "service_account_email" {
  value = google_service_account.mlops_sa.email
}

output "artifact_registry" {
  value = google_artifact_registry_repository.mlops_repo.repository_uri
}

output "bucket" {
  value = google_storage_bucket.mlops_bucket.url
}

output "endpoint_id" {
  value = google_vertex_ai_endpoint.mlops_endpoint.id
}
