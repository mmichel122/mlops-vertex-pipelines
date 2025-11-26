from kfp import dsl
from google_cloud_pipeline_components import aiplatform as gcc_aip

@dsl.component
def train_op(dataset_path: str, model_output: str, project: str, region: str):

    job = gcc_aip.CustomTrainingJobRunOp(
        project=project,
        location=region,
        display_name="train-model",
        model_display_name="iris-model",
        args=[f"--dataset={dataset_path}", f"--output={model_output}"],
        worker_pool_specs=[{
            "machine_spec": {"machine_type": "n1-standard-4"},
            "replica_count": 1,
            "container_spec": {
                "image_uri": f"{region}-docker.pkg.dev/{project}/mlops/train:latest"
            },
        }],
    )

    return job.outputs["model"]
