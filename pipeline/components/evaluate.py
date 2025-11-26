from kfp import dsl
from google_cloud_pipeline_components import aiplatform as gcc_aip

@dsl.component
def evaluate_op(model_path: str, project: str, region: str):

    job = gcc_aip.CustomTrainingJobRunOp(
        project=project,
        location=region,
        display_name="evaluate-model",
        args=[
            f"--model_path={model_path}",
            "--metrics_output=/metrics/metrics.json",
            "--cm_output=/metrics/confusion_matrix.png"
        ],
        worker_pool_specs=[{
            "machine_spec": {"machine_type": "n1-standard-2"},
            "replica_count": 1,
            "container_spec": {
                "image_uri": f"{region}-docker.pkg.dev/{project}/mlops/train:latest"
            },
        }],
    )

    return {
        "metrics": job.outputs["metrics"],
        "cm": job.outputs["artifact"]
    }
