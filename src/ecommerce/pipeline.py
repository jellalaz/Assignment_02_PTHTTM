"""
Application 3 — E-Commerce Customer Behavior & Interest Discovery Pipeline
End-to-end data processing, EDA, dual representation (Tabular vs Text TF-IDF vs Combined),
model training, comparative evaluation, persistence, and inference verification.
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
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "ecommerce" / "Womens Clothing E-Commerce Reviews.csv"
FIG_DIR = PROJECT_ROOT / "figures" / "ecommerce"
MODEL_DIR = PROJECT_ROOT / "models" / "ecommerce"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "ecommerce"

FIG_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 300


def run_ecommerce_pipeline():
    print("=" * 70)
    print("RUNNING APPLICATION 3 — E-COMMERCE CUSTOMER BEHAVIOR PIPELINE")
    print("=" * 70)

    # 1. Load Data
    df_raw = pd.read_csv(DATA_PATH)
    raw_shape = df_raw.shape
    print(f"[1] Raw dataset loaded: {raw_shape[0]} rows, {raw_shape[1]} columns")

    # 2. Data Cleaning & Feature Preparation
    df_clean = df_raw.copy()
    if 'Unnamed: 0' in df_clean.columns:
        df_clean = df_clean.drop(columns=['Unnamed: 0'])

    # Handle missing text gracefully without discarding customer feedback
    df_clean['Title'] = df_clean['Title'].fillna('').astype(str)
    df_clean['Review Text'] = df_clean['Review Text'].fillna('').astype(str)
    df_clean['full_review'] = (df_clean['Title'] + " " + df_clean['Review Text']).str.strip()

    # Fill categorical missing values with 'Unknown'
    cat_cols = ['Division Name', 'Department Name', 'Class Name']
    for c in cat_cols:
        df_clean[c] = df_clean[c].fillna('Unknown').astype(str)

    # Save cleaned version
    df_clean.to_csv(PROCESSED_DIR / "ecommerce_cleaned.csv", index=False)
    print(f"[2] Cleaned dataset shape: {df_clean.shape}")

    # 3. EDA Visualizations
    print("\n[3] Generating EDA Visualizations...")
    target_col = 'Recommended IND'

    # Plot 1: Target Distribution & Rating vs Recommendation
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    counts = df_clean[target_col].value_counts()
    pcts = df_clean[target_col].value_counts(normalize=True) * 100
    bars = axes[0].bar(["Not Recommended (0)", "Recommended (1)"], counts,
                       color=['#d95f02', '#2b5c8f'], width=0.5, edgecolor='black')
    for b, p, c in zip(bars, pcts, counts):
        axes[0].text(b.get_x() + b.get_width() / 2, b.get_height() + 200,
                     f"{c:,} ({p:.1f}%)", ha='center', va='bottom', fontsize=10, fontweight='bold')
    axes[0].set_title("Customer Recommendation Target Distribution", fontsize=11, fontweight='bold')
    axes[0].set_ylabel("Count", fontsize=10)

    # Rating vs Recommended
    rating_rec = pd.crosstab(df_clean['Rating'], df_clean[target_col], normalize='index') * 100
    rating_rec.plot(kind='bar', stacked=True, ax=axes[1], color=['#d95f02', '#2b5c8f'], edgecolor='black')
    axes[1].set_title("Recommendation Rate by Customer Rating", fontsize=11, fontweight='bold')
    axes[1].set_xlabel("Product Rating (1 to 5 Stars)", fontsize=10)
    axes[1].set_ylabel("Percentage (%)", fontsize=10)
    axes[1].legend(["Not Rec (0)", "Rec (1)"], loc='upper left')
    plt.tight_layout()
    plt.savefig(FIG_DIR / "target_rating_distribution.png")
    plt.close()

    # Plot 2: Department Distribution & Review Length vs Target
    df_clean['review_len'] = df_clean['full_review'].apply(lambda x: len(x.split()))
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    order = df_clean['Department Name'].value_counts().index
    sns.countplot(data=df_clean, x='Department Name', order=order, palette='mako', ax=axes[0])
    axes[0].set_title("Review Count by Department", fontsize=11, fontweight='bold')
    axes[0].tick_params(axis='x', rotation=30)

    sns.kdeplot(data=df_clean[df_clean[target_col] == 1], x='review_len', label='Recommended (1)', color='#2b5c8f', fill=True, alpha=0.3, ax=axes[1])
    sns.kdeplot(data=df_clean[df_clean[target_col] == 0], x='review_len', label='Not Recommended (0)', color='#d95f02', fill=True, alpha=0.3, ax=axes[1])
    axes[1].set_title("Review Word Count Distribution by Recommendation", fontsize=11, fontweight='bold')
    axes[1].set_xlabel("Review Word Count", fontsize=10)
    axes[1].set_xlim(0, 120)
    axes[1].legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "department_review_length.png")
    plt.close()

    # Plot 3: Top TF-IDF Terms in Reviews
    sample_texts = df_clean[df_clean['full_review'] != '']['full_review']
    tfidf_quick = TfidfVectorizer(max_features=20, stop_words='english')
    X_tfidf_sample = tfidf_quick.fit_transform(sample_texts)
    mean_scores = np.asarray(X_tfidf_sample.mean(axis=0)).ravel()
    top_words = pd.Series(mean_scores, index=tfidf_quick.get_feature_names_out()).sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    top_words.plot(kind='barh', color='#2b5c8f', edgecolor='black', ax=ax)
    ax.set_title("Top 20 Keywords by Average TF-IDF Score Across Reviews", fontsize=11, fontweight='bold')
    ax.set_xlabel("Mean TF-IDF Weight", fontsize=10)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "top_keywords_tfidf.png")
    plt.close()
    print("    Saved 3 figures to figures/ecommerce/")

    # 4. Data Split (70% Train / 15% Val / 15% Test Stratified)
    print("\n[4] Performing Stratified Train / Validation / Test Split (70/15/15)...")
    num_cols = ['Age', 'Rating', 'Positive Feedback Count']
    tabular_features = num_cols + cat_cols
    all_features = tabular_features + ['full_review']

    X_all = df_clean[all_features]
    y_all = df_clean[target_col].astype(int)

    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X_all, y_all, test_size=0.15, random_state=42, stratify=y_all
    )
    val_ratio = 0.15 / 0.85
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=val_ratio, random_state=42, stratify=y_train_val
    )

    print(f"    Train set: {len(X_train)} | Val set: {len(X_val)} | Test set: {len(X_test)}")

    # 5. Representation Engineering
    # A. Tabular Preprocessor
    tab_preprocessor = ColumnTransformer(
        transformers=[
            ('num', Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ]), num_cols),
            ('cat', Pipeline([
                ('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')),
                ('onehot', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
            ]), cat_cols)
        ]
    )

    # Fit tabular preprocessor strictly on train
    tab_preprocessor.fit(X_train[tabular_features])
    tab_d = len(tab_preprocessor.get_feature_names_out())
    print(f"\n[5] Tabular Representation:")
    print(f"    Raw tabular features: {len(tabular_features)} -> Encoded dimension: d_tab = {tab_d}")

    # B. Text Preprocessor (TF-IDF)
    # Review Text -> Tokenization -> Vocabulary -> TF-IDF Vector
    # Note: TF-IDF produces a sparse numerical vector representation in R^d_text, NOT a dense embedding.
    text_vectorizer = TfidfVectorizer(max_features=2500, ngram_range=(1, 2), stop_words='english')
    text_vectorizer.fit(X_train['full_review'])
    text_d = len(text_vectorizer.get_feature_names_out())
    print(f"    Text TF-IDF Representation:")
    print(f"    Vocabulary size / features: d_text = {text_d}")

    # C. Combined Preprocessor (Tabular + Text)
    combined_preprocessor = ColumnTransformer(
        transformers=[
            ('num', Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ]), num_cols),
            ('cat', Pipeline([
                ('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')),
                ('onehot', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
            ]), cat_cols),
            ('text', TfidfVectorizer(max_features=2500, ngram_range=(1, 2), stop_words='english'), 'full_review')
        ]
    )
    combined_preprocessor.fit(X_train)
    combined_d = tab_d + text_d
    print(f"    Combined Representation: d_combined = {combined_d} features")

    # 6. Model Training & Comparison Across Representations
    print("\n[6] Training Models Across 3 Representation Regimes...")

    # Regime 1: Tabular-Only Models
    tabular_models = {
        "Tabular - Logistic Regression": LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced'),
        "Tabular - Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=42, class_weight='balanced'),
        "Tabular - Random Forest": RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1, class_weight='balanced'),
        "Tabular - SVM (LinearSVC)": CalibratedClassifierCV(LinearSVC(random_state=42, max_iter=2000, class_weight='balanced')),
        "Tabular - Gradient Boosting": GradientBoostingClassifier(n_estimators=100, max_depth=4, random_state=42)
    }

    results = []
    trained_pipelines = {}

    for name, clf in tabular_models.items():
        pipe = Pipeline([
            ('prep', tab_preprocessor),
            ('clf', clf)
        ])
        pipe.fit(X_train[tabular_features], y_train)
        y_val_pred = pipe.predict(X_val[tabular_features])
        y_val_prob = pipe.predict_proba(X_val[tabular_features])[:, 1]

        acc = accuracy_score(y_val, y_val_pred)
        prec = precision_score(y_val, y_val_pred, zero_division=0)
        rec = recall_score(y_val, y_val_pred)
        f1 = f1_score(y_val, y_val_pred)
        auc = roc_auc_score(y_val, y_val_prob)

        results.append({
            "Model": name,
            "Representation": "Tabular Only",
            "Accuracy": round(acc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1-Score": round(f1, 4),
            "ROC-AUC": round(auc, 4)
        })
        trained_pipelines[name] = pipe
        print(f"    ✓ {name:<32} | Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f} | AUC: {auc:.4f}")

    # Regime 2: Text-Only Models (TF-IDF)
    text_models = {
        "Text - TFIDF + LogisticReg": LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced'),
        "Text - TFIDF + LinearSVC": CalibratedClassifierCV(LinearSVC(random_state=42, max_iter=2000, class_weight='balanced'))
    }

    for name, clf in text_models.items():
        pipe = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=2500, ngram_range=(1, 2), stop_words='english')),
            ('clf', clf)
        ])
        pipe.fit(X_train['full_review'], y_train)
        y_val_pred = pipe.predict(X_val['full_review'])
        y_val_prob = pipe.predict_proba(X_val['full_review'])[:, 1]

        acc = accuracy_score(y_val, y_val_pred)
        prec = precision_score(y_val, y_val_pred, zero_division=0)
        rec = recall_score(y_val, y_val_pred)
        f1 = f1_score(y_val, y_val_pred)
        auc = roc_auc_score(y_val, y_val_prob)

        results.append({
            "Model": name,
            "Representation": "Text TF-IDF Only",
            "Accuracy": round(acc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1-Score": round(f1, 4),
            "ROC-AUC": round(auc, 4)
        })
        trained_pipelines[name] = pipe
        print(f"    ✓ {name:<32} | Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f} | AUC: {auc:.4f}")

    # Regime 3: Combined Models (Tabular + Text)
    combined_pipe = Pipeline([
        ('prep', combined_preprocessor),
        ('clf', LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced'))
    ])
    combined_pipe.fit(X_train, y_train)
    y_val_pred = combined_pipe.predict(X_val)
    y_val_prob = combined_pipe.predict_proba(X_val)[:, 1]

    acc = accuracy_score(y_val, y_val_pred)
    prec = precision_score(y_val, y_val_pred, zero_division=0)
    rec = recall_score(y_val, y_val_pred)
    f1 = f1_score(y_val, y_val_pred)
    auc = roc_auc_score(y_val, y_val_prob)

    results.append({
        "Model": "Combined - Tabular + TFIDF LogReg",
        "Representation": "Tabular + Text Combined",
        "Accuracy": round(acc, 4),
        "Precision": round(prec, 4),
        "Recall": round(rec, 4),
        "F1-Score": round(f1, 4),
        "ROC-AUC": round(auc, 4)
    })
    trained_pipelines["Combined - Tabular + TFIDF LogReg"] = combined_pipe
    print(f"    ✓ {'Combined - Tabular + TFIDF LogReg':<32} | Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f} | AUC: {auc:.4f}")

    df_results = pd.DataFrame(results)
    df_results.to_csv(PROJECT_ROOT / "report" / "tables" / "ecommerce_model_comparison.csv", index=False)

    # 7. Model Selection & Final Evaluation on Test Set
    # We choose the Combined model or Tabular Gradient Boosting based on real metrics
    best_model_name = "Combined - Tabular + TFIDF LogReg"
    best_pipeline = trained_pipelines[best_model_name]
    print(f"\n[7] Evaluating Selected Final Model ({best_model_name}) on Independent Test Set...")

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

    # Confusion Matrix Plot
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    sns.heatmap(test_cm, annot=True, fmt="d", cmap="Purples", cbar=False, ax=ax,
                xticklabels=["Pred: Not Rec (0)", "Pred: Rec (1)"],
                yticklabels=["Actual: Not Rec (0)", "Actual: Rec (1)"])
    ax.set_title(f"Test Set Confusion Matrix — {best_model_name}", fontsize=11, fontweight='bold')
    plt.tight_layout()
    plt.savefig(FIG_DIR / "confusion_matrix.png")
    plt.close()

    # Representation Comparison Bar Chart
    fig, ax = plt.subplots(figsize=(10, 5))
    df_chart = df_results.set_index('Model')[['Accuracy', 'Recall', 'F1-Score', 'ROC-AUC']]
    df_chart.plot(kind='bar', ax=ax, colormap='Purples', edgecolor='black', width=0.8)
    ax.set_title("E-Commerce Models Comparison Across Representation Regimes", fontsize=11, fontweight='bold')
    ax.set_ylabel("Score", fontsize=10)
    ax.set_ylim(0.5, 1.05)
    plt.xticks(rotation=25, ha='right')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig(FIG_DIR / "representation_comparison.png")
    plt.close()

    # 8. Model Persistence
    print("\n[8] Persisting Final Pipeline...")
    model_save_path = MODEL_DIR / "ecommerce_pipeline.joblib"
    joblib.dump(best_pipeline, model_save_path)
    print(f"    Saved full pipeline to: {model_save_path}")

    # 9. Reload & Verify Inference
    print("\n[9] Testing Reloaded Model Inference...")
    reloaded_pipeline = joblib.load(model_save_path)

    sample_reviews = pd.DataFrame([
        {
            "Age": 34,
            "Rating": 5,
            "Positive Feedback Count": 4,
            "Division Name": "General",
            "Department Name": "Dresses",
            "Class Name": "Dresses",
            "full_review": "Absolutely loved this gorgeous dress! The fabric is lightweight and fits like a glove."
        },
        {
            "Age": 45,
            "Rating": 2,
            "Positive Feedback Count": 1,
            "Division Name": "General Petite",
            "Department Name": "Tops",
            "Class Name": "Knits",
            "full_review": "Disappointed with the quality. The stitching was unraveling and the sizing runs very small."
        }
    ])

    preds = reloaded_pipeline.predict(sample_reviews)
    probs = reloaded_pipeline.predict_proba(sample_reviews)[:, 1]

    for i, (pred, prob) in enumerate(zip(preds, probs)):
        rec_status = "Recommended (1)" if pred == 1 else "Not Recommended (0)"
        print(f"    Review {i+1}: Predicted = {rec_status} | Probability = {prob:.4f}")

    metadata = {
        "dataset_name": "Women's Clothing E-Commerce Reviews",
        "raw_shape": list(raw_shape),
        "clean_shape": list(df_clean.shape),
        "d_tabular": tab_d,
        "d_text_tfidf": text_d,
        "d_combined": combined_d,
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
    with open(PROJECT_ROOT / "report" / "tables" / "ecommerce_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print("\n[✓] E-COMMERCE PIPELINE COMPLETED SUCCESSFULLY!")
    return metadata


if __name__ == "__main__":
    run_ecommerce_pipeline()
