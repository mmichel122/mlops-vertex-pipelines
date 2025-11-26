import json
import yaml
from kfp import dsl

from google_cloud_pipeline_components.v1 import aiplatform as gcc_aip

from kfp.dsl import Input, Output, Model

from components.preprocess import preprocess_op
from components.train import train_op
from components.evaluate import evaluate_op
from components.deploy import deploy_op

# ---------------- LOAD CONFIG ----------------
with open("pipeline/config.yaml") as f:
    cfg = yaml.safe_load(f)

PROJECT = cfg["project"]
REGION = cfg["region"]
BUCKET = cfg["bucket"]

# ---------------- HELPER COMPONENT ----------------
@dsl.component(base_image="python:3.11")
def compare_accuracy(
    new_metrics_path: dsl.InputPath(str),
    baseline: float,
) -> float:
    with open(new_metrics_path, "r") as f:
        metrics = json.load(f)
    new_acc = metrics["accuracy"]
    print("NEW accuracy:", new_acc)
    print("BASELINE accuracy:", baseline)
    return float(new_acc > baseline)

# ---------------- PIPELINE ----------------
@dsl.pipeline(
    name="vertex-mlops-pipeline",
    pipeline_root=f"{BUCKET}/pipelines",
)
def vertex_pipeline(
    dataset_uri: str = cfg["dataset_uri"],
    endpoint_name: str = cfg["endpoint_name"],
    baseline_accuracy: float = 0.92,
):

    # 1️⃣ PREPROCESS
    preproc = preprocess_op(dataset_uri=dataset_uri)

    # 2️⃣ TRAIN
    model_artifact = train_op(
        dataset_path=preproc.output,
        model_output="/model",
        project=PROJECT,
        region=REGION,
    )

    # 3️⃣ EVALUATE
    eval_artifacts = evaluate_op(
        model_path=model_artifact,
        project=PROJECT,
        region=REGION,
    )

    # 4️⃣ COMPARE ACCURACY
    decision = compare_accuracy(
        new_metrics_path=eval_artifacts["metrics"],
        baseline=baseline_accuracy,
    )

    # 5️⃣ REGISTER MODEL
    upload = gcc_aip.ModelUploadOp(
        project=PROJECT,
        location=REGION,
        display_name="iris-model",
        artifact_uri=model_artifact,
        serving_container_image_uri=(
            "europe-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-4:latest"
        ),
    )

    # 6️⃣ CONDITIONAL DEPLOYMENT
    with dsl.Condition(decision.output == 1.0):
        deploy_op(
            model=upload.outputs["model"],
            endpoint=endpoint_name,
            project=PROJECT,
            region=REGION,
        )

if __name__ == "__main__":
    from kfp import compiler
    compiler.Compiler().compile(
        pipeline_func=vertex_pipeline,
        package_path="pipeline.json",
    )