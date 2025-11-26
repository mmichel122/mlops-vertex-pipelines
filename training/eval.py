import argparse
import json
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import seaborn as sns

def main(args):
    iris = load_iris(as_frame=True)
    df = iris.frame
    df["target"] = iris.target

    X = df.drop("target", axis=1)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = joblib.load(f"{args.model_path}/model.pkl")
    preds = model.predict(X_test)

    acc = accuracy_score(y_test, preds)
    cm = confusion_matrix(y_test, preds)

    metrics = {"accuracy": acc}

    # Write metrics artifact
    with open(args.metrics_output, "w") as f:
        json.dump(metrics, f)

    # Confusion matrix artifact
    plt.figure(figsize=(6,4))
    sns.heatmap(cm, annot=True, cmap="Blues")
    plt.title("Confusion Matrix")
    plt.savefig(args.cm_output)

    print("Evaluation complete")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", required=True)
    parser.add_argument("--metrics_output", default="/metrics/metrics.json")
    parser.add_argument("--cm_output", default="/metrics/confusion_matrix.png")
    args = parser.parse_args()

    main(args)
