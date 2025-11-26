# 🚀 Vertex AI MLOps Pipeline  
**Training → Evaluation → Conditional Deployment → Model Registry → GitHub Actions**

This repository implements a **production-grade MLOps pipeline** on **Vertex AI**, covering:

✔ Automated model training  
✔ Evaluation & metrics tracking  
✔ Model versioning in Vertex AI Model Registry  
✔ Conditional deployment (only when accuracy improves)  
✔ Containerized training jobs  
✔ Pipeline execution via GitHub Actions  
✔ Artifact storage in GCS  

---

## 📁 Repository Structure

vertex-pipelines/
│
├── pipeline/
│ ├── pipeline.py
│ ├── components/
│ │ ├── preprocess.py
│ │ ├── train.py
│ │ ├── evaluate.py
│ │ └── deploy.py
│ └── config.yaml
│
├── training/
│ ├── docker/
│ │ ├── Dockerfile
│ │ └── requirements.txt
│ ├── train.py
│ └── eval.py
│
└── .github/workflows/
└── vertex_pipeline.yaml

---

## 🧱 Components Overview

| Component | Purpose |
|----------|---------|
| `preprocess.py` | Loads & prepares dataset (GCS or local) |
| `train.py` | Runs a Vertex Custom Training Job using your container |
| `evaluate.py` | Computes accuracy + confusion matrix |
| `deploy.py` | Deploys model to a Vertex AI Endpoint |
| `compare_accuracy` | Only deploy if accuracy improves |

---

## 🚀 How the Pipeline Works

### **1. Preprocess**
Loads dataset → stores artifact.

### **2. Train**
Runs training inside a custom container:
europe-west4-docker.pkg.dev/<PROJECT>/mlops/train:latest

markdown
Copier le code
Outputs `model.pkl`.

### **3. Evaluate**
Generates:
- `metrics.json`
- `confusion_matrix.png`

### **4. Compare Accuracy**
Deploy **only if**:
new_accuracy > baseline_accuracy

### **5. Register Model**
Uploads to Vertex AI Model Registry.

### **6. Deploy**
Deploys model to an existing endpoint:
iris-classification-endpoint

---

## ⚙️ Build & Push Training Container

cd training/docker
gcloud builds submit --tag
europe-west4-docker.pkg.dev/<PROJECT>/mlops/train:latest

---

## 🔁 Triggering via GitHub Actions

On push to `main`, your workflow:

- Builds pipeline
- Submits Vertex AI Pipeline run
- Displays run ID in logs

Secrets needed:
GCP_SA_KEY

---

## ▶️ Running Pipeline Manually

python3 -m venv venv
source venv/bin/activate
pip install kfp google-cloud-aiplatform pyyaml

python pipeline/pipeline.py

gcloud ai pipelines run
--project=<PROJECT>
--region=europe-west4
--pipeline-name=vertex-mlops
--file=pipeline.json

---

## 📦 Outputs

Artifacts stored in:
gs://mlops-vertex-playground/pipelines/<run-id>/

Models stored in Vertex AI Model Registry:
Models → iris-model → Versions

---

## 🧠 Notes

- Designed for enterprise-grade MLOps learning.
- Mirrors Google Cloud ML Architect best practices.
- All code is modular, testable, and easily extendable.

---

## 🤝 Need More?

I can generate:

- Terraform for GCP infra  
- Monitoring dashboards  
- CI/CD for image build + pipeline run  
- Endpoint canary release strategy  
- Multi-model A/B testing  

Just tell me: **“add monitoring”**, **“add terraform infra”**, or **“add CI/CD image build”**.