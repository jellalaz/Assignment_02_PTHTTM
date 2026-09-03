# DATASETS.md — Kaggle Datasets Specification & Verification

This document records the exact details of the three real Kaggle datasets downloaded and used for Assignment 02.

---

## 1. Application 1 — Diabetes Prediction

- **Dataset Name:** Diabetes Prediction Dataset
- **Kaggle URL:** https://www.kaggle.com/datasets/ghnshymsaini/diabetes-prediction-dataset
- **Kaggle Slug:** `ghnshymsaini/diabetes-prediction-dataset`
- **Downloaded File:** `data/raw/diabetes/diabetes_prediction_dataset.csv` (3,810,356 bytes)
- **Kaggle Version:** Version 1
- **Download Method:** `kagglehub.dataset_download("ghnshymsaini/diabetes-prediction-dataset")`
- **Environment:** `ai-env` (Python 3.12.13)
- **Observations ($N$):** 100,000
- **Attributes ($d$):** 9 (8 input features + 1 target)
- **Target Variable:** `diabetes` (Integer: `0` = non-diabetic, `1` = diabetic)
- **Observation Unit:** One clinical patient record containing demographic and physiological metrics.
- **Features:**
  1. `gender`: Categorical (`Female`, `Male`, `Other`)
  2. `age`: Float/Numerical (years, ranging 0.08 to 80.0)
  3. `hypertension`: Binary integer (`0` = no, `1` = yes)
  4. `heart_disease`: Binary integer (`0` = no, `1` = yes)
  5. `smoking_history`: Categorical (`never`, `No Info`, `current`, `former`, `ever`, `not current`)
  6. `bmi`: Float/Numerical (Body Mass Index)
  7. `HbA1c_level`: Float/Numerical (Hemoglobin A1c level, %)
  8. `blood_glucose_level`: Integer/Numerical (mg/dL)
  9. `diabetes`: Target variable (`0` or `1`)

---

## 2. Application 2 — House Price Prediction

- **Dataset Name:** House Price Prediction Dataset (2000 Rows)
- **Kaggle URL:** https://www.kaggle.com/datasets/chershi/house-price-prediction-dataset-2000-rows
- **Kaggle Slug:** `chershi/house-price-prediction-dataset-2000-rows`
- **Downloaded File:** `data/raw/house_price/enhanced_house_price_dataset.csv` (152,824 bytes)
- **Kaggle Version:** Version 1
- **Download Method:** `kagglehub.dataset_download("chershi/house-price-prediction-dataset-2000-rows")`
- **Environment:** `ai-env` (Python 3.12.13)
- **Observations ($N$):** 2,000
- **Attributes ($d$):** 16 (15 input features + 1 target)
- **Target Variable:** `Price` (Continuous numerical, real estate property valuation)
- **Observation Unit:** One residential house listing with physical and locational attributes.
- **Features:**
  1. `Area`: Numerical (square feet)
  2. `Bedrooms`: Numerical (count)
  3. `Bathrooms`: Numerical (count)
  4. `Stories`: Numerical (number of floors)
  5. `Parking`: Numerical (parking space capacity)
  6. `Age`: Numerical (property age in years)
  7. `City`: Categorical (metro/city location)
  8. `Furnishing`: Categorical (`Furnished`, `Semi-Furnished`, `Unfurnished`)
  9. `Main Road`: Categorical (`yes` / `no`)
  10. `Guest Room`: Categorical (`yes` / `no`)
  11. `Basement`: Categorical (`yes` / `no`)
  12. `Water Supply`: Categorical
  13. `Air Conditioning`: Categorical (`yes` / `no`)
  14. `Preferred Tenant`: Categorical
  15. `Locality Rating`: Numerical / Ordinal (rating scale)
  16. `Price`: Target variable (house sale price)

---

## 3. Application 3 — Women's E-Commerce Clothing Reviews

- **Dataset Name:** Women's Clothing E-Commerce Reviews
- **Kaggle URL:** https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews
- **Kaggle Slug:** `nicapotato/womens-ecommerce-clothing-reviews`
- **Downloaded File:** `data/raw/ecommerce/Womens Clothing E-Commerce Reviews.csv` (8,483,448 bytes)
- **Kaggle Version:** Version 1
- **Download Method:** `kagglehub.dataset_download("nicapotato/womens-ecommerce-clothing-reviews")`
- **Environment:** `ai-env` (Python 3.12.13)
- **Observations ($N$):** 23,486
- **Attributes ($d$):** 11 (including index and identifier)
- **Target Variable:** `Recommended IND` (Binary integer: `1` = recommended, `0` = not recommended)
- **Observation Unit:** One customer review for an e-commerce clothing product.
- **Features:**
  1. `Unnamed: 0`: Arbitrary integer index (dropped during preprocessing)
  2. `Clothing ID`: Categorical / Integer product identifier
  3. `Age`: Numerical (customer age in years)
  4. `Title`: Text (review title)
  5. `Review Text`: Free-form natural language customer review
  6. `Rating`: Numerical / Ordinal (customer product score 1 to 5)
  7. `Recommended IND`: Target binary classification variable (`0` or `1`)
  8. `Positive Feedback Count`: Numerical (number of other customers who found review positive)
  9. `Division Name`: Categorical (e.g., General, General Petite, Initmates)
  10. `Department Name`: Categorical (e.g., Tops, Dresses, Bottoms, Intimate, Jackets, Trend)
  11. `Class Name`: Categorical (e.g., Dresses, Blouses, Knits, Pants, Sweaters, etc.)

---

## Summary Comparison Table

| Application | Dataset Name | Raw Rows | Raw Cols | Target | Problem Type |
|---|---|---|---|---|---|
| **Diabetes** | Diabetes Prediction Dataset | 100,000 | 9 | `diabetes` | Binary Classification |
| **House Price** | House Price Prediction Dataset (2000 Rows) | 2,000 | 16 | `Price` | Regression |
| **E-Commerce** | Women's Clothing E-Commerce Reviews | 23,486 | 11 | `Recommended IND` | Binary Classification (Tabular + NLP) |
