from kfp import dsl
from google_cloud_pipeline_components import aiplatform as gcc_aip

@dsl.component
def deploy_op(model: str, endpoint: str, project: str, region: str):

    deploy = gcc_aip.EndpointDeployModelOp(
        project=project,
        location=region,
        model=model,
        endpoint=endpoint,
        deployed_model_display_name="iris-auto-deploy",
        traffic_split={"0": 100},
    )
    return deploy.outputs["deployed_model"]
