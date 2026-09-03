# Intelligent System Development Pipeline 🚀

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4.1-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.12-008CC1?logo=neo4j&logoColor=white)](https://neo4j.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://docker.com)

**Posts and Telecommunications Institute of Technology (PTIT)**  
**Course:** Intelligent System Development (Phát triển các hệ thống thông minh)  
**Instructor:** Dinh Que Tran, Ph.D., Assoc. Prof.  

---

## 🎯 1. Overview & Applications

This project implements a complete, end-to-end intelligent system pipeline bridging the gap between raw datasets and deployable, production-ready web services.

$$\text{Raw Data} \longrightarrow \text{Clean} \longrightarrow \text{Represent} \longrightarrow \text{Learn} \longrightarrow \text{Evaluate} \longrightarrow \text{Deploy}$$

The system integrates **three highly diverse intelligent applications**, utilizing both tabular and natural language processing techniques on **100% real Kaggle datasets**:

### 🩺 A. Diabetes Prediction (Clinical Classification)
- **Dataset:** 100,000 patient records (Imbalanced).
- **Techniques:** Standard Scaling, One-Hot Encoding, SMOTE / Balanced Weights.
- **Best Model:** **Random Forest Classifier** (Recall = 89.70%, ROC-AUC = 0.9743).
- **Business Value:** Prevents false negatives in early diabetes screening.

### 🏠 B. House Price Prediction (Real Estate Regression)
- **Dataset:** 2,000 highly diverse property records.
- **Techniques:** Outlier removal, Feature correlation mapping.
- **Best Model:** **Gradient Boosting Regressor** ($R^2 = 0.7448$, MAE = $126,793).
- **Business Value:** Provides highly accurate real estate valuations based on structural and locational data.

### 🛍️ C. E-Commerce Customer Behavior (Multimodal Classification)
- **Dataset:** 23,486 women's clothing reviews (Text + Tabular data).
- **Techniques:** **TF-IDF Vectorization** (Text) + Standard Scaling (Tabular) combined via `ColumnTransformer`.
- **Best Model:** **Logistic Regression** on Combined Features (Accuracy = 93.41%, ROC-AUC = 0.9737).
- **Business Value:** Automatically classifies customer sentiment and product recommendation status from unstructured review text.

---

## 🌐 2. Advanced Extension: Neo4j Knowledge Graph (Graph RAG)

Traditional Machine Learning treats data as isolated rows. To push the boundaries of this E-commerce module, we designed a **Knowledge Graph Architecture** utilizing **Neo4j**.

By converting tabular data into an interconnected graph (`Customer` $\rightarrow$ `WROTE` $\rightarrow$ `Review` $\rightarrow$ `ABOUT` $\rightarrow$ `Product`), the system is primed for **Graph RAG (Retrieval-Augmented Generation)**, allowing a Chatbot to answer complex questions like: *"What do women under 30 think about our summer dresses?"*

- **Setup Guide:** See [NEO4J_SETUP_GUIDE.md](NEO4J_SETUP_GUIDE.md).
- **Cypher Constraints:** Located in `scripts/import_graph.cypher`.
- **Python Driver Demo:** Run `python scripts/neo4j_demo.py` to wipe, build, and simulate a Graph RAG query on your local database.

---

## 🏗️ 3. System Architecture & Deployment

The system is deployed using a modern, decoupled architecture:

1. **Inference Engine (FastAPI):** Exposes `/predict/diabetes`, `/predict/house`, and `/predict/ecommerce` endpoints. Models are pre-loaded into RAM via a `lifespan` context manager ensuring sub-10ms latency.
2. **Data Validation:** Pydantic `v2` enforces strict type checking on all incoming JSON payloads.
3. **Frontend Dashboard:** A responsive, Glassmorphism-styled Web UI (HTML/CSS/JS) that interacts asynchronously with the FastAPI backend via the `Fetch API`.
4. **Mobile LAN Access:** The web dashboard is highly responsive and fully accessible via smartphone over a local Wi-Fi network (Mobile-first viewport).

---

## 🚀 4. Quickstart Guide

### Step 1: Environment Setup
This project strictly requires the `ai-env` Conda environment (Python 3.12).
```bash
conda activate ai-env
pip install -r requirements.txt
```

### Step 2: Download & Process Datasets
```bash
# Downloads raw datasets from Kaggle to data/raw/
python scripts/download_datasets.py

# Execute pipelines to clean data and train models (exports .joblib to models/)
python src/diabetes/pipeline.py
python src/house_price/pipeline.py
python src/ecommerce/pipeline.py
```

### Step 3: Launch the API & Web Server
Run the FastAPI application bound to `0.0.0.0` for LAN access:
```bash
PYTHONPATH=. uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
- **Web Dashboard:** [http://localhost:8000/](http://localhost:8000/)
- **Swagger UI (API Docs):** [http://localhost:8000/docs](http://localhost:8000/docs)

### Step 4: Docker Deployment (Optional)
A highly optimized `Dockerfile` and `render.yaml` are provided for cloud deployment.
```bash
docker build -t intelligent-system .
docker run -p 8000:8000 -e PORT=8000 intelligent-system
```

---

## 📸 5. Automated Screenshots & Documentation
All visual evidence (Desktop UI, Mobile Viewports, Swagger API) is automatically generated using Selenium Headless Chrome. See the `screenshots/` directory.

An exhaustive **84-page Technical Report** (`report/Baocao.pdf`) is dynamically compiled using Python `python-docx`, intertwining data methodology, code snippets, and EDA visualizations.
