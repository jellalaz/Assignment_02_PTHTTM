# Assignment 02 Checklist & Progress Tracking

## Phase 1: Environment & Project Setup
- [x] Verify `ai-env` Python executable, pip, and Jupyter kernel
- [x] Create project directory structure
- [x] Write `requirements.txt`
- [x] Install required packages in `ai-env` (`fastapi`, `uvicorn`, `kagglehub`, `python-multipart`, `pytest`)
- [x] Register `ai-env` ipykernel for Jupyter notebooks
- [x] Freeze environment dependencies to `environment_freeze.txt`

## Phase 2: Kaggle Dataset Download & Verification
- [x] Write `scripts/download_datasets.py`
- [x] Download App 1: `ghnshymsaini/diabetes-prediction-dataset`
- [x] Download App 2: `chershi/house-price-prediction-dataset-2000-rows`
- [x] Download App 3: `nicapotato/womens-ecommerce-clothing-reviews`
- [x] Inspect raw CSV files (rows, columns, dtypes, missing values)
- [x] Create `DATASETS.md` with verified dataset statistics

## Phase 3: Application 1 — Diabetes Prediction
- [x] Implement data loading, cleaning & representation in `src/diabetes/pipeline.py`
- [x] Perform EDA and save figures to `figures/diabetes/`
- [x] Independent train/val/test split (70/15/15 stratified)
- [x] Train DummyClassifier baseline and 5 models (Logistic Regression, KNN, Decision Tree, Random Forest, SVM)
- [x] Evaluate metrics (Accuracy, Precision, Recall, F1, ROC-AUC, Confusion Matrix)
- [x] Persist trained pipeline to `models/diabetes/diabetes_pipeline.joblib`
- [x] Reload model and verify inference test
- [x] Build comprehensive notebook `notebooks/01_diabetes.ipynb`
- [x] Execute notebook `01_diabetes.ipynb` with `ai-env` kernel

## Phase 4: Application 2 — House Price Prediction
- [x] Implement data loading, cleaning & representation in `src/house_price/pipeline.py`
- [x] Perform EDA and save figures to `figures/house_price/`
- [x] Independent train/val/test split (70/15/15)
- [x] Train DummyRegressor baseline and 5 models (Linear Regression, Ridge, Decision Tree, Random Forest, Gradient Boosting)
- [x] Evaluate metrics (MAE, MSE, RMSE, R², Residuals)
- [x] Persist trained pipeline to `models/house_price/house_pipeline.joblib`
- [x] Reload model and verify inference test
- [x] Build comprehensive notebook `notebooks/02_house_price.ipynb`
- [x] Execute notebook `02_house_price.ipynb` with `ai-env` kernel

## Phase 5: Application 3 — E-Commerce Customer Behavior & Interest Discovery
- [x] Implement data loading, cleaning & dual representation in `src/ecommerce/pipeline.py`
- [x] Clarify TF-IDF numerical text representation vs theoretical embeddings
- [x] Perform EDA and save figures to `figures/ecommerce/`
- [x] Independent train/val/test split (70/15/15 stratified)
- [x] Train tabular models, text TF-IDF models, and combined ColumnTransformer model
- [x] Evaluate metrics and compare tabular vs text vs combined
- [x] Persist trained pipeline to `models/ecommerce/ecommerce_pipeline.joblib`
- [x] Reload model and verify inference test
- [x] Build comprehensive notebook `notebooks/03_ecommerce.ipynb`
- [x] Execute notebook `03_ecommerce.ipynb` with `ai-env` kernel

## Phase 6: Unified REST API (FastAPI)
- [x] Implement `api/main.py` with lifespan model loading and `/predict/*` endpoints
- [x] Define Pydantic request/response schemas in `api/schemas.py`
- [x] Write unit and smoke tests in `api/test_api.py`
- [x] Run pytest to verify all endpoints return 200 OK and expected predictions

## Phase 7: Responsive Web Application
- [x] Build modern responsive UI in `web/` (HTML, CSS, JS with relative API endpoints)
- [x] Ensure mobile-first responsive layout (no horizontal overflow, single-column on mobile)
- [x] Test desktop view and take screenshots (`screenshots/web/`)
- [x] Test Swagger UI `/docs` and take screenshots (`screenshots/api/`)

## Phase 8: Mobile Demonstration (Responsive Mobile Web via LAN)
- [x] Test responsive layout at 390x844 smartphone viewport
- [x] Capture mobile screenshots (`screenshots/mobile/`)
- [x] Create `MOBILE_ACCESS_GUIDE.md` for LAN Wi-Fi access (`0.0.0.0:8000`)

## Phase 9: Report & Documentation
- [x] Write `report/report_notes.md` following official 10-chapter structure
- [x] Write `report/discussion_questions.md` answering all 15 core + 6 e-commerce questions
- [x] Create `screenshots/README.md` catalog
- [x] Write comprehensive `README.md`
- [x] Create `FINAL_CHECKLIST.md`

## Phase 10: Optional Neo4j Extension & Final Verification
- [x] Create Neo4j graph demo script `scripts/neo4j_demo.py` & `scripts/import_graph.cypher`
- [x] Write `NEO4J_SETUP_GUIDE.md`
- [x] Run end-to-end smoke tests and verify final checklist

## Phase 11: Official Report Generation & Verification
- [x] Backup original report to `report/Baocao_backup.docx`
- [x] Preserve original cover page in `report/Baocao.docx`
- [x] Implement report generator `scripts/generate_report_docx.py`
- [x] Generate full official technical report `report/Baocao.docx` (552 paragraphs, 6 tables, 31 figures/screenshots)
- [x] Export and verify `report/Baocao.pdf` (54 pages, flawless layout, intact cover)
- [x] Visually audit rendered pages (Cover, TOC, EDA figures, Model tables, Confusion matrices, API/Web/Mobile screenshots)

