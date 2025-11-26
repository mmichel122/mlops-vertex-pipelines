# 🚀 Vertex AI MLOps Pipeline

**Training → Evaluation → Conditional Deployment → Model Registry → GitHub Actions**

This repository implements a **production-grade MLOps pipeline** on **Google Cloud Vertex AI**, including:

* Automated model training
* Evaluation and metrics logging
* Conditional deployment (only if accuracy improves)
* Model versioning in Vertex AI Model Registry
* Containerized training jobs
* Pipeline execution via GitHub Actions
* Artifact storage in GCS

---

## 📁 Repository Structure

```
vertex-pipelines/
│
├── pipeline/
│   ├── pipeline.py
│   ├── components/
│   │   ├── preprocess.py
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   └── deploy.py
│   └── config.yaml
│
├── training/
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── train.py
│   └── eval.py
│
└── .github/workflows/
    └── vertex_pipeline.yaml
```

---

## 🧱 Components Overview

| Component                               | Purpose                                                    |
| --------------------------------------- | ---------------------------------------------------------- |
| `preprocess.py`                         | Loads and prepares dataset (GCS or local)                  |
| `train.py`                              | Launches a Vertex Custom Training Job using your container |
| `evaluate.py`                           | Computes accuracy + confusion matrix                       |
| `deploy.py`                             | Deploys model to a Vertex AI Endpoint                      |
| `compare_accuracy` (inside pipeline.py) | Decides whether new model should be deployed               |

---

## 🚀 How the Pipeline Works

### **1. Preprocess**

Loads dataset (GCS or fallback Iris dataset) and stores a cleaned artifact.

### **2. Train**

Runs your training code inside a custom container:

```
europe-west4-docker.pkg.dev/<PROJECT>/mlops/train:latest
```

Outputs a trained model:

```
model.pkl
```

### **3. Evaluate**

Generates evaluation artifacts:

* `metrics.json`
* `confusion_matrix.png`

### **4. Compare Accuracy**

Deployment occurs **only if:**

```
new_accuracy > baseline_accuracy
```

### **5. Register Model**

Uploads the new model to **Vertex AI Model Registry**.

### **6. Deploy**

Deploys to an existing Vertex endpoint:

```
iris-classification-endpoint
```

Traffic is switched 100% to the new model.

---

## ⚙️ Build & Push Training Container

```bash
cd training/docker

gcloud builds submit --tag \
  europe-west4-docker.pkg.dev/<PROJECT>/mlops/train:latest
```

---

## 🔁 Triggering via GitHub Actions

When pushing to `main`, the workflow will:

1. Build & push training Docker image
2. Compile the Vertex AI Pipeline
3. Submit a pipeline job
4. Display pipeline run ID in the logs

Required secret:

```
GCP_SA_KEY
```

---

## ▶️ Running Pipeline Manually

```bash
python3 -m venv venv
source venv/bin/activate
pip install kfp google-cloud-aiplatform pyyaml

python pipeline/pipeline.py

gcloud ai pipelines run \
  --project=<PROJECT> \
  --region=europe-west4 \
  --pipeline-name=vertex-mlops \
  --file=pipeline.json
```

---

## 📦 Outputs

Artifacts stored in:

```
gs://mlops-vertex-playground/pipelines/<run-id>/
```

Models stored in Vertex AI:

```
Models → iris-model → Versions
```

---

## 🧠 Notes

* Designed for enterprise-grade MLOps learning.
* Mirrors real-world Google Cloud ML Architect best practices.
* Code follows modular, testable, and extensible architecture.

---

## 🤝 Need More?

I can add:

* Terraform infrastructure
* Monitoring dashboards (Vertex AI Monitoring)
* CI/CD for container image build + pipeline run
* Canary deployments / blue-green
* Multi-model A/B testing

Just ask: **“add monitoring”**, **“add terraform infra”**, or **“add CI/CD image build”**.
