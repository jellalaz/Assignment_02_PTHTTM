# Assignment 02: From Data Representation to Deployable Intelligent Systems

**Posts and Telecommunications Institute of Technology (PTIT)**  
**Course:** Intelligent System Development / Phát triển các hệ thống thông minh  
**Instructor:** Dinh Que Tran, Ph.D., Assoc. Prof.  
**Environment:** `ai-env` (Conda Python 3.12.13)  
**Dataset Source:** 100% Real Kaggle Datasets (No synthetic data)

---

## 1. Overview & Applications

This project implements an end-to-end intelligent system pipeline:
$$\text{Raw Data} \longrightarrow \text{Understand} \longrightarrow \text{Clean} \longrightarrow \text{Represent} \longrightarrow \text{Learn} \longrightarrow \text{Evaluate} \longrightarrow \text{Persist} \longrightarrow \text{Deploy}$$

Covering three intelligent applications:
1. **Diabetes Prediction (Clinical Tabular Classification):**
   - **Dataset:** `ghnshymsaini/diabetes-prediction-dataset` (100,000 patient records).
   - **Target:** `diabetes` ($0$ = Non-diabetic, $1$ = Diabetic).
   - **Best Model:** **Random Forest Classifier** (Recall = 89.70%, ROC-AUC = 0.9743 on test set).
2. **House Price Prediction (Real Estate Tabular Regression):**
   - **Dataset:** `chershi/house-price-prediction-dataset-2000-rows` (2,000 property records).
   - **Target:** `Price` (USD valuation).
   - **Best Model:** **Gradient Boosting Regressor** ($R^2 = 0.7448$, MAE = $126,793.85 on test set).
3. **E-Commerce Customer Behavior & Interest Discovery (Multimodal Tabular + NLP Classification):**
   - **Dataset:** `nicapotato/womens-ecommerce-clothing-reviews` (23,486 clothing reviews).
   - **Target:** `Recommended IND` ($1$ = Recommended, $0$ = Not Recommended).
   - **Best Model:** **Combined Tabular + TF-IDF Logistic Regression** (ROC-AUC = 0.9737, Accuracy = 93.41% on test set).

---

## 2. Project Directory Structure

```text
Assignment_02/
├── data/
│   ├── raw/
│   │   ├── diabetes/diabetes_prediction_dataset.csv
│   │   ├── house_price/enhanced_house_price_dataset.csv
│   │   └── ecommerce/Womens Clothing E-Commerce Reviews.csv
│   └── processed/
│       ├── diabetes/diabetes_cleaned.csv
│       ├── house_price/house_price_cleaned.csv
│       └── ecommerce/ecommerce_cleaned.csv
├── notebooks/
│   ├── 01_diabetes.ipynb          # Executed with ai-env kernel (25 sections)
│   ├── 02_house_price.ipynb       # Executed with ai-env kernel (25 sections)
│   └── 03_ecommerce.ipynb         # Executed with ai-env kernel (25 sections)
├── src/
│   ├── diabetes/pipeline.py       # Diabetes training & evaluation pipeline
│   ├── house_price/pipeline.py    # House price regression pipeline
│   └── ecommerce/pipeline.py      # E-Commerce multimodal pipeline
├── models/
│   ├── diabetes/diabetes_pipeline.joblib
│   ├── house_price/house_pipeline.joblib
│   └── ecommerce/ecommerce_pipeline.joblib
├── api/
│   ├── main.py                    # Unified FastAPI REST API & Web Server
│   ├── schemas.py                 # Pydantic v2 validation models
│   └── test_api.py                # Automated pytest suite (100% pass)
├── web/
│   ├── templates/index.html       # Responsive Web dashboard template
│   └── static/
│       ├── css/style.css          # Sleek glassmorphism dark theme
│       └── js/app.js              # Relative API client controller
├── screenshots/
│   ├── web/                       # Desktop verification screenshots (1280x900)
│   ├── mobile/                    # Responsive mobile screenshots (390x844 viewport)
│   ├── api/                       # Swagger UI documentation screenshots
│   └── README.md                  # Catalog mapping screenshots to report sections
├── figures/                       # High-resolution EDA and evaluation PNG charts
│   ├── diabetes/
│   ├── house_price/
│   └── ecommerce/
├── report/
│   ├── report_notes.md            # Comprehensive 9-chapter technical report
│   ├── discussion_questions.md    # Authentic answers to all 21 discussion questions
│   └── tables/                    # CSV & JSON evaluation metadata tables
├── scripts/
│   ├── download_datasets.py       # Kagglehub automated dataset download
│   ├── capture_all_screenshots.py # Selenium headless browser automation
│   └── neo4j_demo.py              # Optional Neo4j graph demonstration
├── TODO.md                        # Granular progress checklist
├── DATASETS.md                    # Verified dataset profiles and shapes
├── requirements.txt               # Project dependency specification
├── environment_freeze.txt         # Exact pip freeze snapshot
├── MOBILE_ACCESS_GUIDE.md         # LAN Wi-Fi setup guide for mobile devices
├── NEO4J_SETUP_GUIDE.md           # Neo4j setup and Cypher graph queries
└── FINAL_CHECKLIST.md             # Honest deliverable compliance audit
```

---

## 3. Installation & Environment Setup

This project is strictly configured to run in the **`ai-env`** Conda environment:

```bash
# 1. Activate the environment
conda activate ai-env

# 2. Verify Python executable and pip
which python
# Output: /home/jellalaz/miniconda3/envs/ai-env/bin/python

# 3. Install required dependencies
pip install -r requirements.txt
```

---

## 4. Download Datasets

To download and extract all three Kaggle datasets into `data/raw/`:
```bash
python scripts/download_datasets.py
```

---

## 5. Run ML Pipelines & Execute Notebooks

To retrain all models, generate high-resolution figures, and export persisted `.joblib` pipelines:
```bash
python src/diabetes/pipeline.py
python src/house_price/pipeline.py
python src/ecommerce/pipeline.py
```

To re-execute all three Jupyter Notebooks from start to finish with the `ai-env` kernel:
```bash
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=ai-env --ExecutePreprocessor.timeout=-1 notebooks/01_diabetes.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=ai-env --ExecutePreprocessor.timeout=-1 notebooks/02_house_price.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=ai-env --ExecutePreprocessor.timeout=-1 notebooks/03_ecommerce.ipynb
```

---

## 6. Run API & Responsive Web Server

Launch the unified FastAPI server bound to `0.0.0.0` (accessible from both localhost and LAN devices):
```bash
PYTHONPATH=. /home/jellalaz/miniconda3/envs/ai-env/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

- **Web Application Dashboard:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive Swagger Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health Check:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## 7. Automated API Testing

Run the automated test suite:
```bash
PYTHONPATH=. /home/jellalaz/miniconda3/envs/ai-env/bin/pytest api/test_api.py -v
```
All 6 tests verify `200 OK` status, Pydantic schema validation, and expected inference outputs.

---

## 8. Mobile LAN Demonstration

As requested, the mobile experience is implemented as a **Responsive Mobile Web Client** accessible over the local Wi-Fi network:
1. Ensure the server is running on `0.0.0.0:8000`.
2. Find the host machine LAN IP: `hostname -I` (e.g., `192.168.0.105`).
3. Connect a smartphone to the same Wi-Fi and navigate to:
   ```text
   http://192.168.0.105:8000/
   ```
4. Full instructions are provided in [MOBILE_ACCESS_GUIDE.md](file:///home/jellalaz/Documents/Jellalaz/DATA_CODE/PYTHON/Assignment_02/MOBILE_ACCESS_GUIDE.md).

---

## 9. Captured Evidence Screenshots

All screenshots were automatically captured from the live application using Selenium with Chrome Headless:
- **Desktop Web:** `screenshots/web/web_home.png`, `diabetes_web_result.png`, `house_web_result.png`, `ecommerce_web_result.png`.
- **Mobile Viewport (390x844):** `screenshots/mobile/mobile_home.png`, `diabetes_mobile.png`, `house_mobile.png`, `ecommerce_mobile.png`.
- **Swagger API Docs:** `screenshots/api/swagger_docs.png`, `api_diabetes_result.png`, `api_house_result.png`, `api_ecommerce_result.png`.

Detailed mappings are documented in [screenshots/README.md](file:///home/jellalaz/Documents/Jellalaz/DATA_CODE/PYTHON/Assignment_02/screenshots/README.md).
