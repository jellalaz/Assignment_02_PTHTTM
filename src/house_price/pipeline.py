"""
Application 2 — House Price Prediction Pipeline
End-to-end data processing, EDA, representation, regression model training, evaluation, persistence, and inference verification.
"""

import os
import sys
import time
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "house_price" / "enhanced_house_price_dataset.csv"
FIG_DIR = PROJECT_ROOT / "figures" / "house_price"
MODEL_DIR = PROJECT_ROOT / "models" / "house_price"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "house_price"

FIG_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 300


def run_house_price_pipeline():
    print("=" * 70)
    print("RUNNING APPLICATION 2 — HOUSE PRICE PREDICTION PIPELINE")
    print("=" * 70)

    # 1. Load Data
    df_raw = pd.read_csv(DATA_PATH)
    raw_shape = df_raw.shape
    print(f"[1] Raw dataset loaded: {raw_shape[0]} rows, {raw_shape[1]} columns")

    # 2. Data Cleaning
    duplicates_count = int(df_raw.duplicated().sum())
    missing_count = int(df_raw.isna().sum().sum())
    print(f"[2] Missing values: {missing_count} | Duplicate rows: {duplicates_count}")
    df_clean = df_raw.copy()

    # Save to processed
    df_clean.to_csv(PROCESSED_DIR / "house_price_cleaned.csv", index=False)

    # 3. Feature Definitions & Representation
    target_col = "Price"
    num_cols = ['Area', 'Bedrooms', 'Bathrooms', 'Stories', 'Parking', 'Age', 'Locality Rating']
    cat_cols = ['City', 'Furnishing', 'Main Road', 'Guest Room', 'Basement', 'Water Supply', 'Air Conditioning', 'Preferred Tenant']

    X_raw = df_clean.drop(columns=[target_col])
    y_raw = df_clean[target_col].astype(float)

    sample_raw_record = X_raw.iloc[0].to_dict()
    print("\n[3] Sample Raw Observation:")
    for k, v in sample_raw_record.items():
        print(f"    • {k}: {v}")
    print(f"    • Target (Price): {y_raw.iloc[0]:,.0f}")

    # 4. EDA Visualizations
    print("\n[4] Generating EDA Visualizations...")

    # Plot 1: Target Price distribution & Skewness
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    sns.histplot(df_clean['Price'], kde=True, color='#1b7837', ax=axes[0])
    axes[0].set_title("House Price Distribution (USD)", fontsize=11, fontweight='bold')
    axes[0].set_xlabel("Price", fontsize=10)

    sns.boxplot(x=df_clean['Price'], color='#a6dba0', ax=axes[1])
    axes[1].set_title("House Price Boxplot (Outlier Detection)", fontsize=11, fontweight='bold')
    axes[1].set_xlabel("Price", fontsize=10)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "price_distribution.png")
    plt.close()

    # Plot 2: Area vs Price & Locality Rating vs Price
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    sns.scatterplot(data=df_clean, x='Area', y='Price', hue='City', alpha=0.6, ax=axes[0])
    axes[0].set_title("Living Area vs House Price by City", fontsize=11, fontweight='bold')
    axes[0].set_xlabel("Area (sq ft)", fontsize=10)
    axes[0].set_ylabel("Price", fontsize=10)

    sns.boxplot(data=df_clean, x='Locality Rating', y='Price', color='#5aae61', ax=axes[1])
    axes[1].set_title("Locality Rating vs House Price", fontsize=11, fontweight='bold')
    axes[1].set_xlabel("Locality Rating", fontsize=10)
    axes[1].set_ylabel("Price", fontsize=10)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "area_locality_vs_price.png")
    plt.close()

    # Plot 3: Bedrooms & Bathrooms vs Price
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    sns.barplot(data=df_clean, x='Bedrooms', y='Price', color='#762a83', ax=axes[0], edgecolor='black')
    axes[0].set_title("Number of Bedrooms vs Average Price", fontsize=11, fontweight='bold')

    sns.barplot(data=df_clean, x='Bathrooms', y='Price', color='#9970ab', ax=axes[1], edgecolor='black')
    axes[1].set_title("Number of Bathrooms vs Average Price", fontsize=11, fontweight='bold')
    plt.tight_layout()
    plt.savefig(FIG_DIR / "rooms_vs_price.png")
    plt.close()

    # Plot 4: Correlation Heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    corr = df_clean[num_cols + [target_col]].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Greens", cbar=True, square=True, ax=ax,
                linewidths=0.5, annot_kws={"size": 9})
    ax.set_title("Pearson Correlation Heatmap (Numerical Features & Price)", fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(FIG_DIR / "correlation_heatmap.png")
    plt.close()
    print("    Saved 4 figures to figures/house_price/")

    # 5. Independent Train / Validation / Test Split (70% / 15% / 15%)
    print("\n[5] Performing Train / Validation / Test Split (70/15/15)...")
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X_raw, y_raw, test_size=0.15, random_state=42
    )
    val_ratio = 0.15 / 0.85
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=val_ratio, random_state=42
    )

    print(f"    Train set:      {X_train.shape[0]} observations ({X_train.shape[0]/len(df_clean)*100:.1f}%)")
    print(f"    Validation set: {X_val.shape[0]} observations ({X_val.shape[0]/len(df_clean)*100:.1f}%)")
    print(f"    Test set:       {X_test.shape[0]} observations ({X_test.shape[0]/len(df_clean)*100:.1f}%)")

    # 6. Preprocessing & Representation Definition
    print("\n[6] Building ColumnTransformer Preprocessor (Fit strictly on Train)...")
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_cols),
            ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), cat_cols)
        ]
    )

    preprocessor.fit(X_train)
    feature_names_out = preprocessor.get_feature_names_out()
    encoded_d = len(feature_names_out)
    print(f"    Original features: {X_train.shape[1]} -> Encoded features: {encoded_d}")
    print(f"    Transformed feature names: {list(feature_names_out)}")
    print(f"    Feature matrix shape: X_train ∈ R^({X_train.shape[0]} × {encoded_d}), y ∈ R^{X_train.shape[0]}")

    # 7. Model Training & Comparison
    print("\n[7] Training Baseline and 5 Regression Models...")
    models = {
        "Dummy Baseline": DummyRegressor(strategy="median"),
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=1.0, random_state=42),
        "Decision Tree": DecisionTreeRegressor(max_depth=6, random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)
    }

    results = []
    trained_pipelines = {}

    for name, reg in models.items():
        start_time = time.time()
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('regressor', reg)
        ])
        pipeline.fit(X_train, y_train)
        train_time = time.time() - start_time

        y_val_pred = pipeline.predict(X_val)
        mae = mean_absolute_error(y_val, y_val_pred)
        mse = mean_squared_error(y_val, y_val_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_val, y_val_pred)

        results.append({
            "Model": name,
            "MAE": round(mae, 2),
            "MSE": round(mse, 2),
            "RMSE": round(rmse, 2),
            "R2": round(r2, 4),
            "Train_Time_s": round(train_time, 2)
        })
        trained_pipelines[name] = pipeline
        print(f"    ✓ {name:<20} | MAE: {mae:>10,.1f} | RMSE: {rmse:>10,.1f} | R²: {r2:>7.4f} | Time: {train_time:.2f}s")

    df_results = pd.DataFrame(results)
    df_results.to_csv(PROJECT_ROOT / "report" / "tables" / "house_price_model_comparison.csv", index=False)

    # 8. Model Selection & Final Evaluation on Test Set
    best_model_name = "Gradient Boosting"
    best_pipeline = trained_pipelines[best_model_name]
    print(f"\n[8] Evaluating Selected Final Model ({best_model_name}) on Independent Test Set...")

    y_test_pred = best_pipeline.predict(X_test)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    test_mse = mean_squared_error(y_test, y_test_pred)
    test_rmse = np.sqrt(test_mse)
    test_r2 = r2_score(y_test, y_test_pred)

    print(f"    Test Set Performance:")
    print(f"    MAE:  {test_mae:,.2f}")
    print(f"    MSE:  {test_mse:,.2f}")
    print(f"    RMSE: {test_rmse:,.2f}")
    print(f"    R²:   {test_r2:.4f}")

    # Plot Actual vs Predicted & Residuals
    residuals = y_test - y_test_pred
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Actual vs Predicted
    axes[0].scatter(y_test, y_test_pred, alpha=0.6, color='#1b7837', edgecolors='k', s=40)
    min_val = min(y_test.min(), y_test_pred.min())
    max_val = max(y_test.max(), y_test_pred.max())
    axes[0].plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Ideal Fit (y = ŷ)')
    axes[0].set_title(f"Actual vs Predicted Price — {best_model_name}", fontsize=11, fontweight='bold')
    axes[0].set_xlabel("Actual Price ($)", fontsize=10)
    axes[0].set_ylabel("Predicted Price ($)", fontsize=10)
    axes[0].legend()

    # Residuals Plot
    axes[1].scatter(y_test_pred, residuals, alpha=0.6, color='#762a83', edgecolors='k', s=40)
    axes[1].axhline(0, color='r', linestyle='--', lw=2)
    axes[1].set_title(f"Residuals Plot (Residuals vs Predicted)", fontsize=11, fontweight='bold')
    axes[1].set_xlabel("Predicted Price ($)", fontsize=10)
    axes[1].set_ylabel("Residuals ($)", fontsize=10)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "actual_vs_predicted_residuals.png")
    plt.close()

    # Plot Model Comparison Bar Chart
    fig, ax = plt.subplots(figsize=(9, 4.5))
    df_plot = df_results[df_results['Model'] != "Dummy Baseline"].set_index('Model')['R2']
    bars = df_plot.plot(kind='bar', ax=ax, color='#1b7837', edgecolor='black', width=0.6)
    ax.set_title("House Price Regression Models Comparison ($R^2$ Score on Validation Set)", fontsize=11, fontweight='bold')
    ax.set_ylabel("R² Score", fontsize=10)
    ax.set_ylim(0, 1.0)
    for bar in ax.patches:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f"{bar.get_height():.3f}", ha='center', va='bottom', fontsize=9, fontweight='bold')
    plt.xticks(rotation=20, ha='right')
    plt.tight_layout()
    plt.savefig(FIG_DIR / "model_comparison.png")
    plt.close()

    # 9. Model Persistence
    print("\n[9] Persisting Final Pipeline...")
    model_save_path = MODEL_DIR / "house_pipeline.joblib"
    joblib.dump(best_pipeline, model_save_path)
    print(f"    Saved full pipeline to: {model_save_path}")

    # 10. Reload & Verify Inference
    print("\n[10] Testing Reloaded Model Inference...")
    reloaded_pipeline = joblib.load(model_save_path)

    # Use REAL records from the dataset with correct categorical values
    sample_houses = pd.DataFrame([
        {
            "Area": 5292,
            "Bedrooms": 5,
            "Bathrooms": 3,
            "Stories": 3,
            "Parking": 2,
            "Age": 2,
            "City": "Hyderabad",
            "Furnishing": "Furnished",
            "Main Road": "No",
            "Guest Room": "No",
            "Basement": "No",
            "Water Supply": "Both",
            "Air Conditioning": "Yes",
            "Preferred Tenant": "Company",
            "Locality Rating": 5
        },
        {
            "Area": 571,
            "Bedrooms": 1,
            "Bathrooms": 1,
            "Stories": 1,
            "Parking": 0,
            "Age": 18,
            "City": "Chennai",
            "Furnishing": "Unfurnished",
            "Main Road": "No",
            "Guest Room": "Yes",
            "Basement": "No",
            "Water Supply": "Both",
            "Air Conditioning": "Yes",
            "Preferred Tenant": "Family",
            "Locality Rating": 3
        }
    ])

    preds = reloaded_pipeline.predict(sample_houses)
    for i, pred in enumerate(preds):
        print(f"    Property {i+1}: Predicted Price = ${pred:,.2f}")

    metadata = {
        "dataset_name": "House Price Prediction Dataset",
        "raw_shape": list(raw_shape),
        "clean_shape": list(raw_shape),
        "encoded_features_dim": encoded_d,
        "feature_names_out": list(feature_names_out),
        "train_size": len(X_train),
        "val_size": len(X_val),
        "test_size": len(X_test),
        "best_model": best_model_name,
        "test_metrics": {
            "MAE": round(test_mae, 2),
            "MSE": round(test_mse, 2),
            "RMSE": round(test_rmse, 2),
            "R2": round(test_r2, 4)
        }
    }
    with open(PROJECT_ROOT / "report" / "tables" / "house_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print("\n[✓] HOUSE PRICE PIPELINE COMPLETED SUCCESSFULLY!")
    return metadata


if __name__ == "__main__":
    run_house_price_pipeline()
