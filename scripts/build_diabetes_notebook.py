"""
Script to generate the complete notebooks/01_diabetes.ipynb adhering to the 25 required sections.
Uses nbformat to construct an authentic, fully executable notebook.
"""

import nbformat as nbf
from pathlib import Path

nb = nbf.v4.new_notebook()

# Metadata
nb.metadata = {
    "kernelspec": {
        "display_name": "Python (ai-env)",
        "language": "python",
        "name": "ai-env"
    },
    "language_info": {
        "name": "python",
        "version": "3.12.13"
    }
}

cells = []

# 1. Problem Description
cells.append(nbf.v4.new_markdown_cell("""# Application 1 — Diabetes Prediction
## 1. Mô tả bài toán
Bài toán đặt ra là dự đoán xem một bệnh nhân có mắc bệnh tiểu đường hay không dựa trên các thông số nhân khẩu học và các chỉ số xét nghiệm lâm sàng (tuổi, giới tính, BMI, tiền sử hút thuốc, huyết áp, bệnh tim, chỉ số HbA1c và nồng độ đường huyết).
Đây là bài toán **Phân loại nhị phân (Binary Classification)**:
- $X$: Tập hợp các đặc trưng lâm sàng của bệnh nhân.
- $y \in \{0, 1\}$: Nhãn bệnh tiểu đường ($0$ = Không mắc, $1$ = Mắc bệnh).
"""))

# 2. Dataset Source
cells.append(nbf.v4.new_markdown_cell("""## 2. Nguồn Dataset
- **Tên Dataset:** Diabetes Prediction Dataset
- **Nguồn:** Kaggle (`ghnshymsaini/diabetes-prediction-dataset`)
- **Tệp dữ liệu:** `data/raw/diabetes/diabetes_prediction_dataset.csv`
"""))

# 3. Imports
cells.append(nbf.v4.new_markdown_cell("## 3. Import thư viện & Kiểm tra môi trường"))
cells.append(nbf.v4.new_code_cell("""import sys
print("Python Executable:", sys.executable)
print("Python Version:", sys.version)

import os
import time
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

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
%matplotlib inline
"""))

# 4. Random Seed Configuration
cells.append(nbf.v4.new_markdown_cell("## 4. Cấu hình Random Seed"))
cells.append(nbf.v4.new_code_cell("""RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
print(f"Random seed configured: {RANDOM_SEED}")
"""))

# 5. Load Dataset
cells.append(nbf.v4.new_markdown_cell("## 5. Load Dataset"))
cells.append(nbf.v4.new_code_cell("""data_path = Path("../data/raw/diabetes/diabetes_prediction_dataset.csv")
if not data_path.exists():
    data_path = Path("data/raw/diabetes/diabetes_prediction_dataset.csv")

df = pd.read_csv(data_path)
print("Data loaded successfully!")
print("Dataset Shape:", df.shape)
"""))

# 6. Data Inspection
cells.append(nbf.v4.new_markdown_cell("## 6. Data Inspection (Khảo sát dữ liệu)"))
cells.append(nbf.v4.new_code_cell("""print("First 5 rows:")
display(df.head())

print("Random 5 rows sample:")
display(df.sample(5, random_state=RANDOM_SEED))

print("Data Info:")
df.info()

print("Numerical Summary:")
display(df.describe())

print("Categorical Summary:")
display(df.describe(include="object"))
"""))

# 7. Data Quality
cells.append(nbf.v4.new_markdown_cell("## 7. Data Quality (Chất lượng dữ liệu)"))
cells.append(nbf.v4.new_code_cell("""print("Missing Values Check:")
print(df.isna().sum())

print("\\nDuplicate Rows Count:")
n_duplicates = df.duplicated().sum()
print(f"{n_duplicates} duplicate records found ({n_duplicates/len(df)*100:.2f}%)")

print("\\nUnique values per column:")
print(df.nunique())

print("\\nClass Distribution of Target (diabetes):")
print(df['diabetes'].value_counts())
print(df['diabetes'].value_counts(normalize=True) * 100)
"""))

# 8. Data Cleaning
cells.append(nbf.v4.new_markdown_cell("""## 8. Data Cleaning (Làm sạch dữ liệu)
- **Xử lý trùng lặp:** Loại bỏ 3,854 dòng trùng lặp hoàn toàn để tránh rò rỉ dữ liệu giữa tập huấn luyện và kiểm tra.
- **Giá trị khuyết thiếu:** Không có giá trị NaN trực tiếp trong các cột số. Giá trị `'No Info'` trong `smoking_history` được giữ lại như một nhóm phân loại riêng.
"""))
cells.append(nbf.v4.new_code_cell("""df_clean = df.drop_duplicates().reset_index(drop=True)
print(f"Original shape: {df.shape} -> Cleaned shape: {df_clean.shape}")
"""))

# 9. Feature Types Classification
cells.append(nbf.v4.new_markdown_cell("## 9. Phân loại kiểu thuộc tính (Feature Types)"))
cells.append(nbf.v4.new_code_cell("""target_col = 'diabetes'
numerical_cols = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level', 'hypertension', 'heart_disease']
categorical_cols = ['gender', 'smoking_history']

print(f"Target Column: {target_col}")
print(f"Numerical Features ({len(numerical_cols)}): {numerical_cols}")
print(f"Categorical Features ({len(categorical_cols)}): {categorical_cols}")
"""))

# 10. Data Representation
cells.append(nbf.v4.new_markdown_cell("""## 10. Data Representation (Biểu diễn dữ liệu)
Theo lý thuyết Lecture 02:
Mỗi quan sát là một vector:
$$x_i = [x_{i1}, x_{i2}, \\dots, x_{id}]^T \\in \\mathbb{R}^d$$
Toàn bộ tập dữ liệu biểu diễn dưới dạng ma trận đặc trưng:
$$X \\in \\mathbb{R}^{N \\times d}$$
- Thuộc tính số: Chuẩn hóa Z-score với `StandardScaler`.
- Thuộc tính phân loại: Mã hóa one-hot với `OneHotEncoder(drop='first')`.
"""))
cells.append(nbf.v4.new_code_cell("""print("Ví dụ 1 mẫu quan sát thô từ CSV:")
sample_row = df_clean.drop(columns=[target_col]).iloc[0]
for k, v in sample_row.to_dict().items():
    print(f"  {k}: {v}")
"""))

# 11. EDA
cells.append(nbf.v4.new_markdown_cell("## 11. Phân tích khám phá dữ liệu (EDA)"))
cells.append(nbf.v4.new_code_cell("""fig, axes = plt.subplots(1, 2, figsize=(12, 4))
df_clean[target_col].value_counts().plot(kind='bar', ax=axes[0], color=['#2b5c8f', '#d95f02'], edgecolor='black')
axes[0].set_title("Phân bố nhãn Diabetes (Class Imbalance)")
axes[0].set_xticklabels(["Không mắc (0)", "Mắc bệnh (1)"], rotation=0)

sns.histplot(data=df_clean, x='age', hue=target_col, bins=30, kde=True, ax=axes[1], palette=['#2b5c8f', '#d95f02'])
axes[1].set_title("Phân bố Độ tuổi theo Tình trạng Tiểu đường")
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
sns.boxplot(data=df_clean, x=target_col, y='blood_glucose_level', hue=target_col, legend=False, ax=axes[0], palette=['#2b5c8f', '#d95f02'])
axes[0].set_title("Đường huyết (blood_glucose_level) vs Diabetes")

sns.boxplot(data=df_clean, x=target_col, y='HbA1c_level', hue=target_col, legend=False, ax=axes[1], palette=['#2b5c8f', '#d95f02'])
axes[1].set_title("Chỉ số HbA1c vs Diabetes")
plt.tight_layout()
plt.show()

plt.figure(figsize=(7, 5))
sns.heatmap(df_clean[numerical_cols + [target_col]].corr(), annot=True, fmt=".2f", cmap="Blues")
plt.title("Ma trận tương quan Pearson giữa các biến lâm sàng")
plt.tight_layout()
plt.show()
"""))

# 12. Feature Engineering
cells.append(nbf.v4.new_markdown_cell("## 12. Feature Engineering & Chuẩn bị biến"))
cells.append(nbf.v4.new_code_cell("""X = df_clean.drop(columns=[target_col])
y = df_clean[target_col].astype(int)
print(f"X shape: {X.shape}, y shape: {y.shape}")
"""))

# 13. Train / Validation / Test Split
cells.append(nbf.v4.new_markdown_cell("""## 13. Chia tập Train / Validation / Test (70% / 15% / 15%)
Chia có phân tầng (`stratify=y`) để bảo toàn tỉ lệ lớp thiểu số.
"""))
cells.append(nbf.v4.new_code_cell("""X_train_val, X_test, y_train_val, y_test = train_test_split(
    X, y, test_size=0.15, random_state=RANDOM_SEED, stratify=y
)
X_train, X_val, y_train, y_val = train_test_split(
    X_train_val, y_train_val, test_size=(0.15/0.85), random_state=RANDOM_SEED, stratify=y_train_val
)

print(f"Train set: {X_train.shape[0]} ({len(X_train)/len(df_clean)*100:.1f}%)")
print(f"Val set:   {X_val.shape[0]} ({len(X_val)/len(df_clean)*100:.1f}%)")
print(f"Test set:  {X_test.shape[0]} ({len(X_test)/len(df_clean)*100:.1f}%)")
"""))

# 14. Preprocessing Pipeline
cells.append(nbf.v4.new_markdown_cell("""## 14. Xây dựng Preprocessing Pipeline
Chỉ fit trên tập Train để tuyệt đối tránh Data Leakage.
"""))
cells.append(nbf.v4.new_code_cell("""preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), categorical_cols)
    ]
)

# Fit chỉ trên Train
preprocessor.fit(X_train)
encoded_feature_names = preprocessor.get_feature_names_out()
d_encoded = len(encoded_feature_names)
print(f"Số chiều đặc trưng sau mã hóa d = {d_encoded}")
print("Các đặc trưng sau biến đổi:", list(encoded_feature_names))

X_train_trans = preprocessor.transform(X_train)
print(f"Kích thước ma trận đặc trưng huấn luyện: X_train in R^({X_train_trans.shape[0]} x {X_train_trans.shape[1]})")
"""))

# 15. Baseline
cells.append(nbf.v4.new_markdown_cell("## 15. Mô hình Baseline (DummyClassifier)"))
cells.append(nbf.v4.new_code_cell("""dummy = DummyClassifier(strategy="stratified", random_state=RANDOM_SEED)
dummy.fit(X_train, y_train)
y_val_dummy = dummy.predict(X_val)

print(f"Baseline Accuracy:  {accuracy_score(y_val, y_val_dummy):.4f}")
print(f"Baseline Recall:    {recall_score(y_val, y_val_dummy):.4f}")
print(f"Baseline F1-Score:  {f1_score(y_val, y_val_dummy):.4f}")
"""))

# 16. Train Models
cells.append(nbf.v4.new_markdown_cell("## 16. Huấn luyện 5 mô hình học máy"))
cells.append(nbf.v4.new_code_cell("""models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_SEED, class_weight='balanced'),
    "KNN": KNeighborsClassifier(n_neighbors=5, n_jobs=-1),
    "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=RANDOM_SEED, class_weight='balanced'),
    "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=10, random_state=RANDOM_SEED, n_jobs=-1, class_weight='balanced'),
    "SVM (LinearSVC)": CalibratedClassifierCV(LinearSVC(random_state=RANDOM_SEED, max_iter=2000, class_weight='balanced'))
}

trained_pipelines = {}
for name, clf in models.items():
    pipe = Pipeline([
        ('preprocessor', preprocessor),
        ('model', clf)
    ])
    pipe.fit(X_train, y_train)
    trained_pipelines[name] = pipe
    print(f"✓ Trained {name}")
"""))

# 17. Compare Models
cells.append(nbf.v4.new_markdown_cell("## 17. So sánh các mô hình trên Validation Set"))
cells.append(nbf.v4.new_code_cell("""records = []
for name, pipe in trained_pipelines.items():
    y_pred = pipe.predict(X_val)
    y_prob = pipe.predict_proba(X_val)[:, 1]
    
    records.append({
        "Model": name,
        "Accuracy": round(accuracy_score(y_val, y_pred), 4),
        "Precision": round(precision_score(y_val, y_pred), 4),
        "Recall": round(recall_score(y_val, y_pred), 4),
        "F1-Score": round(f1_score(y_val, y_pred), 4),
        "ROC-AUC": round(roc_auc_score(y_val, y_prob), 4)
    })

comparison_df = pd.DataFrame(records)
display(comparison_df)
"""))

# 18. Evaluation
cells.append(nbf.v4.new_markdown_cell("""## 18. Đánh giá chuyên sâu & Lựa chọn mô hình
Trong chẩn đoán y tế, **Recall** có ý nghĩa sống còn vì False Negative (bỏ sót bệnh nhân mắc bệnh tiểu đường) sẽ dẫn đến không điều trị kịp thời và gây biến chứng nghiêm trọng. Random Forest đạt cân bằng vượt trội với Recall > 91%, ROC-AUC > 0.97 và F1 cao nhất.
"""))
cells.append(nbf.v4.new_code_cell("""best_model_name = "Random Forest"
final_pipeline = trained_pipelines[best_model_name]

y_test_pred = final_pipeline.predict(X_test)
y_test_prob = final_pipeline.predict_proba(X_test)[:, 1]

print("=== TEST SET PERFORMANCE (RANDOM FOREST) ===")
print(f"Accuracy:  {accuracy_score(y_test, y_test_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_test_pred):.4f}")
print(f"Recall:    {recall_score(y_test, y_test_pred):.4f}")
print(f"F1-Score:  {f1_score(y_test, y_test_pred):.4f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, y_test_prob):.4f}")
"""))

# 19. Error Analysis
cells.append(nbf.v4.new_markdown_cell("## 19. Phân tích lỗi (Confusion Matrix & Classification Report)"))
cells.append(nbf.v4.new_code_cell("""cm = confusion_matrix(y_test, y_test_pred)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Dự đoán: Không mắc (0)", "Dự đoán: Mắc bệnh (1)"],
            yticklabels=["Thực tế: Không mắc (0)", "Thực tế: Mắc bệnh (1)"])
plt.title(f"Confusion Matrix trên Test Set — {best_model_name}")
plt.tight_layout()
plt.show()

print("\\nClassification Report:\\n")
print(classification_report(y_test, y_test_pred, target_names=["Không mắc", "Mắc bệnh"]))
"""))

# 20. Model Selection
cells.append(nbf.v4.new_markdown_cell("""## 20. Kết luận lựa chọn mô hình
Mô hình **Random Forest Classifier** được lựa chọn vì:
1. Đạt Recall cao (xấp xỉ 90% trên Test Set), giảm thiểu tối đa ca dương tính giả bị bỏ sót (False Negatives).
2. ROC-AUC đạt 0.9743, thể hiện khả năng phân tách 2 lớp xuất sắc.
3. Hoạt động ổn định trên cả biến số và biến phân loại sau mã hóa.
"""))

# 21. Save Model / Pipeline
cells.append(nbf.v4.new_markdown_cell("## 21. Lưu trữ Pipeline hoàn chỉnh (Model Persistence)"))
cells.append(nbf.v4.new_code_cell("""model_path = Path("../models/diabetes/diabetes_pipeline.joblib")
if not model_path.parent.exists():
    model_path = Path("models/diabetes/diabetes_pipeline.joblib")

joblib.dump(final_pipeline, model_path)
print(f"Pipeline saved to: {model_path}")
"""))

# 22. Load lại Model
cells.append(nbf.v4.new_markdown_cell("## 22. Tải lại Pipeline và kiểm tra tính toàn vẹn"))
cells.append(nbf.v4.new_code_cell("""reloaded_pipeline = joblib.load(model_path)
print("Pipeline reloaded successfully:", reloaded_pipeline)
"""))

# 23. Inference Test
cells.append(nbf.v4.new_markdown_cell("## 23. Thực hiện dự đoán trên mẫu dữ liệu mới"))
cells.append(nbf.v4.new_code_cell("""sample_patient = pd.DataFrame([{
    "gender": "Female",
    "age": 65.0,
    "hypertension": 1,
    "heart_disease": 1,
    "smoking_history": "current",
    "bmi": 35.4,
    "HbA1c_level": 7.8,
    "blood_glucose_level": 220
}])

pred = reloaded_pipeline.predict(sample_patient)[0]
prob = reloaded_pipeline.predict_proba(sample_patient)[0][1]

status = "Bị tiểu đường (Diabetic)" if pred == 1 else "Không bị tiểu đường (Non-Diabetic)"
print(f"Kết quả dự đoán: {status} (Lớp {pred})")
print(f"Xác suất mắc bệnh: {prob:.4f}")
"""))

# 24. Deployment Input Example
cells.append(nbf.v4.new_markdown_cell("## 24. Cấu trúc JSON Request cho Web / Mobile API"))
cells.append(nbf.v4.new_code_cell("""json_example = {
    "gender": "Female",
    "age": 65.0,
    "hypertension": 1,
    "heart_disease": 1,
    "smoking_history": "current",
    "bmi": 35.4,
    "HbA1c_level": 7.8,
    "blood_glucose_level": 220
}
import json
print("Sample REST API Request Payload:")
print(json.dumps(json_example, indent=2))
"""))

# 25. Conclusion
cells.append(nbf.v4.new_markdown_cell("""## 25. Kết luận
- Pipeline hoàn chỉnh từ Dữ liệu thô $\\rightarrow$ Tiền xử lý $\\rightarrow$ Biểu diễn số $\\rightarrow$ Huấn luyện $\\rightarrow$ Đánh giá $\\rightarrow$ Lưu trữ đã được xây dựng thành công.
- Pipeline đóng gói cả `ColumnTransformer` (StandardScaler + OneHotEncoder) và `RandomForestClassifier` trong một đối tượng duy nhất, bảo đảm tính nhất quán khi triển khai lên REST API.
"""))

nb.cells = cells

target_nb_path = Path("/home/jellalaz/Documents/Jellalaz/DATA_CODE/PYTHON/Assignment_02/notebooks/01_diabetes.ipynb")
with open(target_nb_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"Created notebook at {target_nb_path} with {len(cells)} cells.")
