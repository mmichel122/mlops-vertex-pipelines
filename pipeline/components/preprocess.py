from kfp import dsl
import pandas as pd

@dsl.component(base_image="python:3.11")
def preprocess_op(dataset_uri: str, output_data: dsl.OutputPath("Dataset")):
    import pandas as pd
    import os

    if dataset_uri.startswith("gs://"):
        import tensorflow as tf
        tf.io.gfile.copy(dataset_uri, "/tmp/dataset.csv", overwrite=True)
        df = pd.read_csv("/tmp/dataset.csv")
    else:
        df = pd.read_csv(dataset_uri)

    df.to_csv(output_data, index=False)
