import argparse
import pandas as pd
import joblib
import os
from google.cloud import storage
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

def load_dataset(path: str):
    if path.startswith("gs://"):
        bucket_name, file_path = path[5:].split("/", 1)
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        tmp = "/tmp/dataset.csv"
        blob.download_to_filename(tmp)
        return pd.read_csv(tmp)

    return pd.read_csv(path)

def main(args):
    # Load dataset
    try:
        df = load_dataset(args.dataset)
    except:
        iris = load_iris(as_frame=True)
        df = iris.frame
        df["target"] = iris.target

    X = df.drop("target", axis=1)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save model
    os.makedirs(args.output, exist_ok=True)
    joblib.dump(model, f"{args.output}/model.pkl")

    print(f"Model saved at: {args.output}/model.pkl")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=False)
    parser.add_argument("--output", default="/model")
    args = parser.parse_args()

    main(args)
