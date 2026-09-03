"""
Application 1 — Diabetes Prediction Pipeline
End-to-end data processing, EDA, representation, model training, evaluation, persistence, and inference verification.
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
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "diabetes" / "diabetes_prediction_dataset.csv"
FIG_DIR = PROJECT_ROOT / "figures" / "diabetes"
MODEL_DIR = PROJECT_ROOT / "models" / "diabetes"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "diabetes"

FIG_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Plot styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 300


def run_diabetes_pipeline():
    print("=" * 70)
    print("RUNNING APPLICATION 1 — DIABETES PREDICTION PIPELINE")
    print("=" * 70)

    # 1. Load Data
    df_raw = pd.read_csv(DATA_PATH)
    raw_shape = df_raw.shape
    print(f"[1] Raw dataset loaded: {raw_shape[0]} rows, {raw_shape[1]} columns")

    # 2. Data Cleaning
    duplicates_count = int(df_raw.duplicated().sum())
    print(f"[2] Duplicate rows detected: {duplicates_count}")
    df_clean = df_raw.drop_duplicates().reset_index(drop=True)
    clean_shape = df_clean.shape
    print(f"    After dropping exact duplicates: {clean_shape[0]} rows, {clean_shape[1]} columns")

    # Save cleaned sample to processed
    df_clean.to_csv(PROCESSED_DIR / "diabetes_cleaned.csv", index=False)

    # 3. Feature Definitions & Representation Analysis
    target_col = "diabetes"
    num_cols = ["age", "bmi", "HbA1c_level", "blood_glucose_level", "hypertension", "heart_disease"]
    cat_cols = ["gender", "smoking_history"]

    X_raw = df_clean.drop(columns=[target_col])
    y_raw = df_clean[target_col].astype(int)

    # Display real observation transformation
    sample_raw_record = X_raw.iloc[0].to_dict()
    print("\n[3] Sample Raw Observation:")
    for k, v in sample_raw_record.items():
        print(f"    • {k}: {v}")

    # 4. EDA Visualizations
    print("\n[4] Generating EDA Visualizations...")

    # Plot 1: Target distribution
    fig, ax = plt.subplots(figsize=(6, 4))
    counts = df_clean[target_col].value_counts()
    percentages = df_clean[target_col].value_counts(normalize=True) * 100
    bars = ax.bar(["Non-Diabetic (0)", "Diabetic (1)"], counts, color=['#2b5c8f', '#d95f02'], width=0.5, edgecolor='black')
    for bar, pct, count in zip(bars, percentages, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1000,
                f"{count:,}\n({pct:.1f}%)", ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.set_title("Diabetes Target Class Distribution (Imbalance Analysis)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Patient Count", fontsize=10)
    ax.set_ylim(0, max(counts) * 1.15)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "target_distribution.png")
    plt.close()

    # Plot 2: Age vs Diabetes
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(data=df_clean, x='age', hue=target_col, bins=30, kde=True,
                 palette=['#2b5c8f', '#d95f02'], element='step', common_norm=False, ax=ax)
    ax.set_title("Age Distribution by Diabetes Status", fontsize=12, fontweight='bold')
    ax.set_xlabel("Age (Years)", fontsize=10)
    ax.set_ylabel("Density / Count", fontsize=10)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "age_distribution.png")
    plt.close()

    # Plot 3: Blood Glucose & HbA1c vs Diabetes
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    sns.boxplot(data=df_clean, x=target_col, y='blood_glucose_level', palette=['#2b5c8f', '#d95f02'], ax=axes[0])
    axes[0].set_xticklabels(["Non-Diabetic (0)", "Diabetic (1)"])
    axes[0].set_title("Blood Glucose Level vs Diabetes", fontsize=11, fontweight='bold')
    axes[0].set_ylabel("Blood Glucose Level (mg/dL)", fontsize=10)

    sns.boxplot(data=df_clean, x=target_col, y='HbA1c_level', palette=['#2b5c8f', '#d95f02'], ax=axes[1])
    axes[1].set_xticklabels(["Non-Diabetic (0)", "Diabetic (1)"])
    axes[1].set_title("HbA1c Level vs Diabetes", fontsize=11, fontweight='bold')
    axes[1].set_ylabel("HbA1c Level (%)", fontsize=10)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "glucose_hba1c_distribution.png")
    plt.close()

    # Plot 4: Correlation Heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    num_df = df_clean[num_cols + [target_col]]
    corr = num_df.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", cbar=True, square=True, ax=ax,
                linewidths=0.5, annot_kws={"size": 9})
    ax.set_title("Pearson Correlation Heatmap (Clinical Numerical Features)", fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(FIG_DIR / "correlation_heatmap.png")
    plt.close()

    # Plot 5: BMI Distribution vs Diabetes
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.kdeplot(data=df_clean[df_clean[target_col] == 0], x='bmi', label='Non-Diabetic (0)', color='#2b5c8f', fill=True, alpha=0.3)
    sns.kdeplot(data=df_clean[df_clean[target_col] == 1], x='bmi', label='Diabetic (1)', color='#d95f02', fill=True, alpha=0.3)
    ax.set_title("BMI Density Distribution by Diabetes Diagnosis", fontsize=12, fontweight='bold')
    ax.set_xlabel("Body Mass Index (BMI)", fontsize=10)
    ax.set_xlim(10, 60)
    ax.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "bmi_distribution.png")
    plt.close()
    print("    Saved 5 figures to figures/diabetes/")

    # 5. Independent Train / Validation / Test Split (70% / 15% / 15%)
    print("\n[5] Performing Stratified Train / Validation / Test Split (70/15/15)...")
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X_raw, y_raw, test_size=0.15, random_state=42, stratify=y_raw
    )
    # Split train_val (85%) into train (70% total -> 70/85 = 0.8235) and val (15% total -> 15/85 = 0.1765)
    val_ratio_of_train_val = 0.15 / 0.85
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=val_ratio_of_train_val, random_state=42, stratify=y_train_val
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

    # Fit preprocessor strictly on X_train to prevent any data leakage
    preprocessor.fit(X_train)
    feature_names_out = preprocessor.get_feature_names_out()
    encoded_d = len(feature_names_out)
    print(f"    Original features: {X_train.shape[1]} -> Encoded features: {encoded_d}")
    print(f"    Transformed feature names: {list(feature_names_out)}")
    print(f"    Feature matrix shape: X_train ∈ R^({X_train.shape[0]} × {encoded_d})")

    # Sample representation vector
    x0_transformed = preprocessor.transform(X_train.iloc[[0]])[0]
    print(f"    Sample transformed vector x_0 (first 6 dimensions):\n    {x0_transformed[:6].round(4)}")

    # 7. Model Training & Comparison
    print("\n[7] Training Baseline and 5 Machine Learning Models...")
    models = {
        "Dummy Baseline": DummyClassifier(strategy="stratified", random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced'),
        "KNN": KNeighborsClassifier(n_neighbors=5, n_jobs=-1),
        "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=42, class_weight='balanced'),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1, class_weight='balanced'),
        "SVM (LinearSVC)": CalibratedClassifierCV(LinearSVC(random_state=42, max_iter=2000, class_weight='balanced'))
    }

    results = []
    trained_pipelines = {}

    for name, clf in models.items():
        start_time = time.time()
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', clf)
        ])
        pipeline.fit(X_train, y_train)
        train_time = time.time() - start_time

        # Inference on validation set
        y_val_pred = pipeline.predict(X_val)
        y_val_prob = pipeline.predict_proba(X_val)[:, 1] if hasattr(pipeline, "predict_proba") else None

        acc = accuracy_score(y_val, y_val_pred)
        prec = precision_score(y_val, y_val_pred, zero_division=0)
        rec = recall_score(y_val, y_val_pred)
        f1 = f1_score(y_val, y_val_pred)
        roc = roc_auc_score(y_val, y_val_prob) if y_val_prob is not None else float("nan")

        results.append({
            "Model": name,
            "Accuracy": round(acc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1-Score": round(f1, 4),
            "ROC-AUC": round(roc, 4),
            "Train_Time_s": round(train_time, 2)
        })
        trained_pipelines[name] = pipeline
        print(f"    ✓ {name:<22} | Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f} | AUC: {roc:.4f} | Time: {train_time:.2f}s")

    df_results = pd.DataFrame(results)
    df_results.to_csv(PROJECT_ROOT / "report" / "tables" / "diabetes_model_comparison.csv", index=False)

    # 8. Model Selection & Final Evaluation on Test Set
    # In medical screening for diabetes, Recall is paramount to avoid deadly False Negatives (undiagnosed patients),
    # while maintaining reasonable Precision and top F1 / ROC-AUC.
    # We evaluate candidate models on the untouched Test Set.
    best_model_name = "Random Forest"
    best_pipeline = trained_pipelines[best_model_name]
    print(f"\n[8] Evaluating Selected Final Model ({best_model_name}) on Independent Test Set...")

    y_test_pred = best_pipeline.predict(X_test)
    y_test_prob = best_pipeline.predict_proba(X_test)[:, 1]

    test_acc = accuracy_score(y_test, y_test_pred)
    test_prec = precision_score(y_test, y_test_pred)
    test_rec = recall_score(y_test, y_test_pred)
    test_f1 = f1_score(y_test, y_test_pred)
    test_roc = roc_auc_score(y_test, y_test_prob)
    test_cm = confusion_matrix(y_test, y_test_pred)

    print(f"    Test Set Performance:")
    print(f"    Accuracy:  {test_acc:.4f}")
    print(f"    Precision: {test_prec:.4f}")
    print(f"    Recall:    {test_rec:.4f}")
    print(f"    F1-Score:  {test_f1:.4f}")
    print(f"    ROC-AUC:   {test_roc:.4f}")
    print(f"    Confusion Matrix:\n{test_cm}")

    # Plot Confusion Matrix
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    sns.heatmap(test_cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax,
                xticklabels=["Pred: Non-Diabetic", "Pred: Diabetic"],
                yticklabels=["Actual: Non-Diabetic", "Actual: Diabetic"])
    ax.set_title(f"Test Set Confusion Matrix — {best_model_name}", fontsize=11, fontweight='bold')
    plt.tight_layout()
    plt.savefig(FIG_DIR / "confusion_matrix.png")
    plt.close()

    # Plot Model Comparison Bar Chart
    fig, ax = plt.subplots(figsize=(10, 5))
    df_plot = df_results[df_results['Model'] != "Dummy Baseline"].set_index('Model')[['Accuracy', 'Recall', 'F1-Score', 'ROC-AUC']]
    df_plot.plot(kind='bar', ax=ax, colormap='Blues', edgecolor='black', width=0.75)
    ax.set_title("Diabetes Models Comparison (Validation Metrics)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Score", fontsize=10)
    ax.set_ylim(0, 1.1)
    plt.xticks(rotation=20, ha='right')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig(FIG_DIR / "model_comparison.png")
    plt.close()

    # 9. Model Persistence
    print("\n[9] Persisting Final Pipeline...")
    model_save_path = MODEL_DIR / "diabetes_pipeline.joblib"
    joblib.dump(best_pipeline, model_save_path)
    print(f"    Saved full pipeline to: {model_save_path}")

    # 10. Reload & Verify Inference
    print("\n[10] Testing Reloaded Model Inference...")
    reloaded_pipeline = joblib.load(model_save_path)

    # Test sample: High-risk patient vs Low-risk patient
    sample_patients = pd.DataFrame([
        {
            "gender": "Female",
            "age": 65.0,
            "hypertension": 1,
            "heart_disease": 1,
            "smoking_history": "current",
            "bmi": 35.4,
            "HbA1c_level": 7.8,
            "blood_glucose_level": 220
        },
        {
            "gender": "Male",
            "age": 25.0,
            "hypertension": 0,
            "heart_disease": 0,
            "smoking_history": "never",
            "bmi": 21.2,
            "HbA1c_level": 5.2,
            "blood_glucose_level": 90
        }
    ])

    preds = reloaded_pipeline.predict(sample_patients)
    probs = reloaded_pipeline.predict_proba(sample_patients)[:, 1]

    for i, (pred, prob) in enumerate(zip(preds, probs)):
        status = "Diabetic" if pred == 1 else "Non-Diabetic"
        print(f"    Patient {i+1}: Predicted = {status} ({pred}) | Probability = {prob:.4f}")

    # Save metadata dictionary for report
    metadata = {
        "dataset_name": "Diabetes Prediction Dataset",
        "raw_shape": list(raw_shape),
        "clean_shape": list(clean_shape),
        "duplicates_dropped": duplicates_count,
        "encoded_features_dim": encoded_d,
        "feature_names_out": list(feature_names_out),
        "train_size": len(X_train),
        "val_size": len(X_val),
        "test_size": len(X_test),
        "best_model": best_model_name,
        "test_metrics": {
            "Accuracy": round(test_acc, 4),
            "Precision": round(test_prec, 4),
            "Recall": round(test_rec, 4),
            "F1": round(test_f1, 4),
            "ROC_AUC": round(test_roc, 4),
            "ConfusionMatrix": test_cm.tolist()
        }
    }
    with open(PROJECT_ROOT / "report" / "tables" / "diabetes_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print("\n[✓] DIABETES PIPELINE COMPLETED SUCCESSFULLY!")
    return metadata


if __name__ == "__main__":
    run_diabetes_pipeline()
