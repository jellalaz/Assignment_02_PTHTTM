# -*- coding: utf-8 -*-
"""
Chapter VII: Application 1 — Diabetes Risk Prediction
"""

from docx.enum.text import WD_ALIGN_PARAGRAPH
from .config import (
    add_styled_heading, add_body_p, add_bullet_p, add_code_block, add_code_snippet_with_notes,
    add_styled_table, add_figure_with_notes
)

def build_chapter_7(doc):
    add_styled_heading(doc, "CHƯƠNG VII. ỨNG DỤNG 1 — DỰ ĐOÁN BỆNH TIỂU ĐƯỜNG", 1)

    add_styled_heading(doc, "7.1. Mô tả bài toán", 2)
    add_body_p(doc, "Bệnh đái tháo đường (Diabetes Mellitus) là một bệnh rối loạn chuyển hóa mạn tính nguy hiểm hàng đầu thế giới, đặc trưng bởi sự gia tăng nồng độ đường huyết kéo dài do thiếu hụt tiết insulin hoặc đề kháng insulin. Nếu không được phát hiện và quản lý sớm, bệnh dẫn tới những biến chứng tàn phá nặng nề: suy thận giai đoạn cuối, bệnh võng mạc gây mù lòa, tai biến mạch máu não, xơ vữa động mạch và hoại tử chi dưới dẫn đến đoạn chi.")
    add_body_p(doc, "Mục tiêu của ứng dụng là xây dựng một quy trình học máy hoàn chỉnh có khả năng sàng lọc và dự đoán nguy cơ mắc bệnh tiểu đường ở bệnh nhân dựa trên các chỉ số nhân khẩu học và xét nghiệm lâm sàng định kỳ. Đây là bài toán phân loại nhị phân (Binary Classification):")
    add_bullet_p(doc, "Tập hợp các chỉ số sức khỏe của bệnh nhân bao gồm tuổi, BMI, huyết áp, bệnh tim, nồng độ glucose và HbA1c.", bold_prefix="Tập đặc trưng đầu vào (X): ")
    add_bullet_p(doc, "Tình trạng bệnh tiểu đường, trong đó y = 0 biểu thị người khỏe mạnh (Non-Diabetic) và y = 1 biểu thị người mắc bệnh tiểu đường (Diabetic).", bold_prefix="Biến mục tiêu (y): ")

    add_styled_heading(doc, "7.2. Giới thiệu tập dữ liệu", 2)
    add_body_p(doc, "Hệ thống khai thác tập dữ liệu lâm sàng chính thức từ nền tảng Kaggle: 'Diabetes Prediction Dataset' (tác giả ghnshymsaini). Link dataset: https://www.kaggle.com/datasets/ghnshymsaini/diabetes-prediction-dataset. Tập dữ liệu thô bao gồm đúng 100,000 bản ghi bệnh nhân với 8 đặc trưng đầu vào và 1 nhãn mục tiêu được lưu trữ dưới định dạng bảng CSV.")
    add_code_block(doc,
">>> df = pd.read_csv('data/raw/diabetes/diabetes_prediction_dataset.csv')\n"
">>> df.shape\n"
"(100000, 9)\n\n"
">>> df.head(5)\n"
"   gender   age  hypertension  heart_disease smoking_history    bmi  HbA1c_level  blood_glucose_level  diabetes\n"
"0  Female  80.0             0              1           never  25.19          6.6                  140         0\n"
"1  Female  54.0             0              0         No Info  27.32          6.6                   80         0\n"
"2    Male  28.0             0              0           never  27.32          5.7                  158         0\n"
"3  Female  36.0             0              0         current  23.45          5.0                  155         0\n"
"4    Male  76.0             1              1         current  20.14          4.8                  155         0"
    )

    add_styled_heading(doc, "7.3. Khảo sát và tìm hiểu dữ liệu", 2)
    add_body_p(doc, "Mỗi dòng dữ liệu đại diện cho một hồ sơ bệnh án lâm sàng của một bệnh nhân độc lập. Thống kê chi tiết các thuộc tính:")
    add_styled_table(
        doc,
        "Bảng 7.1. Danh mục các thuộc tính của tập dữ liệu Diabetes Prediction",
        ["Thuộc tính", "Phân loại", "Kiểu dữ liệu", "Miền giá trị", "Ý nghĩa y khoa lâm sàng"],
        [
            ["gender", "Categorical", "object", "Female, Male, Other", "Giới tính sinh học của bệnh nhân"],
            ["age", "Numerical", "float64", "0.08 – 80.0 tuổi", "Tuổi của bệnh nhân tại thời điểm lấy mẫu"],
            ["hypertension", "Numerical (Binary)", "int64", "0 hoặc 1", "Tiền sử bệnh tăng huyết áp mạn tính"],
            ["heart_disease", "Numerical (Binary)", "int64", "0 hoặc 1", "Tiền sử bệnh lý động mạch vành / tim mạch"],
            ["smoking_history", "Categorical", "object", "never, current, former, ever, not current, No Info", "Lịch sử tiếp xúc với khói thuốc lá"],
            ["bmi", "Numerical", "float64", "10.01 – 95.69 kg/m²", "Chỉ số khối cơ thể (Body Mass Index)"],
            ["HbA1c_level", "Numerical", "float64", "3.5 – 9.0 %", "Nồng độ Hemoglobin glycated (đường huyết 3 tháng)"],
            ["blood_glucose_level", "Numerical", "int64", "80 – 300 mg/dL", "Nồng độ đường huyết tức thời tại thời điểm lấy máu"],
            ["diabetes (Target)", "Target", "int64", "0 hoặc 1", "Nhãn mục tiêu: 0 = Khỏe mạnh; 1 = Mắc tiểu đường"]
        ],
        col_widths=[1.4, 1.1, 0.9, 1.3, 2.3],
        align_cols=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    )
    add_body_p(doc, "Phân loại biến: Các thuộc tính số học gồm 6 biến: age, bmi, HbA1c_level, blood_glucose_level, hypertension, heart_disease. Hai thuộc tính phân loại chuỗi là: gender và smoking_history.")

    add_styled_heading(doc, "7.4. Làm sạch dữ liệu", 2)
    add_body_p(doc, "Quá trình làm sạch dữ liệu được thực hiện tuần tự qua các bước kiểm tra nghiêm ngặt:")

    add_styled_heading(doc, "7.4.1. Xử lý giá trị thiếu", 3)
    add_code_block(doc,
">>> df.isnull().sum()\n"
"gender                 0\n"
"age                    0\n"
"hypertension           0\n"
"heart_disease          0\n"
"smoking_history        0\n"
"bmi                    0\n"
"HbA1c_level            0\n"
"blood_glucose_level    0\n"
"diabetes               0\n"
"dtype: int64"
    )
    add_body_p(doc, "Kết quả kiểm tra khẳng định toàn bộ 9 cột đều có 100,000 giá trị hợp lệ, không xuất hiện bất kỳ ô trống (NaN) nào. Do đó không cần áp dụng các thuật toán điền giá trị thiếu nhân tạo.")

    add_styled_heading(doc, "7.4.2. Xử lý bản ghi trùng lặp", 3)
    add_code_block(doc,
">>> duplicate_count = df.duplicated().sum()\n"
">>> print(f'Số lượng bản ghi trùng lặp: {duplicate_count}')\n"
"Số lượng bản ghi trùng lặp: 3854\n\n"
">>> df = df.drop_duplicates()\n"
">>> print(f'Kích thước dữ liệu sạch sau khi lọc trùng: {df.shape}')\n"
"Kích thước dữ liệu sạch sau khi lọc trùng: (96146, 9)"
    )
    add_body_p(doc, "Việc loại bỏ 3,854 bản ghi trùng lặp là bắt buộc để ngăn chặn nguy cơ rò rỉ dữ liệu khi một bệnh nhân bị nhân bản xuất hiện đồng thời trong cả tập Train và tập Test.")

    add_styled_heading(doc, "7.4.3. Xử lý giá trị không hợp lệ", 3)
    add_body_p(doc, "Kiểm tra miền giá trị cho thấy: age dao động từ 0.08 đến 80 tuổi (hợp lệ cho cả bệnh nhi và người cao tuổi); bmi tối thiểu 10.01 đến tối đa 95.69 kg/m²; glucose từ 80 đến 300 mg/dL đều nằm trong giới hạn sinh lý con người. Cột gender ghi nhận 18 ca nhãn 'Other' (<0.02%), được giữ lại và mã hóa nhị phân bình thường.")

    add_styled_heading(doc, "7.5. Biểu diễn dữ liệu", 2)
    add_body_p(doc, "Dữ liệu được chuyển đổi thành các vector số học trước khi đưa vào mô hình học máy:")
    
    code_diab_preprocess = '''num_transformer = StandardScaler()
cat_transformer = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')

preprocessor = ColumnTransformer(transformers=[
    ('num', num_transformer, num_cols),
    ('cat', cat_transformer, cat_cols)
])'''
    add_code_snippet_with_notes(
        doc,
        code_text=code_diab_preprocess,
        caption_text="Đoạn mã 7.1. Tiền xử lý và biểu diễn dữ liệu cho Diabetes Prediction.",
        description_items=[
            "Đoạn mã xây dựng ColumnTransformer để xử lý song song các nhóm biến.",
            "Áp dụng StandardScaler cho các biến số học (tuổi, bmi, glucose) và OneHotEncoder cho các biến danh mục (giới tính, hút thuốc).",
            "Kết quả của bước này trực tiếp tạo ra không gian vector chuẩn hóa dùng để huấn luyện mô hình."
        ],
        source_file="src/diabetes/pipeline.py"
    )

    add_body_p(doc, "Không gian biểu diễn số học được kiến tạo từ hai phân nhóm đặc trưng thông qua ColumnTransformer:")
    add_bullet_p(doc, "Gồm 6 biến: age, bmi, HbA1c_level, blood_glucose_level, hypertension, heart_disease → Áp dụng StandardScaler Z-score → Tạo ra 6 chiều số thực.", bold_prefix="Đặc trưng số học (Numerical): ")
    add_bullet_p(doc, "Gồm gender (loại Female, giữ lại Male và Other → 2 chiều) và smoking_history (loại No Info, giữ lại current, ever, former, never, not current → 5 chiều) → Áp dụng OneHotEncoder(drop='first') → Tạo ra 7 chiều nhị phân.", bold_prefix="Đặc trưng danh mục (Categorical): ")
    add_body_p(doc, "Tổng số chiều không gian vector biểu diễn là: d = 6 + 2 + 5 = 13 chiều. Kích thước toán học của ma trận đặc trưng qua các tập dữ liệu:")
    add_code_block(doc,
"x_i ∈ ℝ^13\n"
"X_train ∈ ℝ^(67,302 × 13),   X_val ∈ ℝ^(14,422 × 13),   X_test ∈ ℝ^(14,422 × 13)"
    )

    add_styled_heading(doc, "7.6. Phân tích khám phá dữ liệu (EDA)", 2)
    add_body_p(doc, "Năm biểu đồ phân tích chuyên sâu được trực quan hóa để bóc tách các quy luật dịch tễ học then chốt:")


    code_diab_dist = '''# Trực quan hóa phân bố nhãn (Target Distribution)
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x='diabetes', palette='Set2')
plt.title("Phân bố bệnh nhân Tiểu đường (Mất cân bằng nhãn)")
plt.xlabel("0: Không mắc bệnh | 1: Mắc bệnh")
plt.ylabel("Số lượng bệnh nhân")
plt.tight_layout()
plt.show()'''

    add_code_snippet_with_notes(
        doc,
        code_text=code_diab_dist,
        caption_text="Đoạn mã 7.4. Trực quan hóa phân bố biến mục tiêu bằng CountPlot.",
        description_items=[
            "Sử dụng sns.countplot để thống kê nhanh số lượng bệnh nhân theo từng nhãn.",
            "Code trực tiếp bộc lộ rõ ràng sự mất cân bằng nghiêm trọng giữa nhãn 0 và nhãn 1, từ đó định hướng cho việc phải sử dụng class_weight='balanced' khi huấn luyện."
        ],
        source_file="notebooks/01_diabetes.ipynb"
    )

    add_figure_with_notes(
        doc,
        "figures/diabetes/target_distribution.png",

        "Hình 7.1. Phân bố biến mục tiêu Diabetes trong tập dữ liệu.",
        [
            "Tập dữ liệu sạch gồm 87,976 mẫu âm tính (Lớp 0 - chiếm 91.5%) và 8,170 mẫu dương tính (Lớp 1 - chiếm 8.5%).",
            "Tỷ lệ mất cân bằng lớp ở mức cực kỳ nghiêm trọng (~11:1)."
        ],
        explanation="Tỷ lệ này phản ánh đúng thực tế dịch tễ học trong cộng đồng, nơi đa số người dân không mắc bệnh.",
        ml_implication="Độ chính xác (Accuracy) hoàn toàn bị vô hiệu hóa vì một mô hình tầm thường đoán tất cả là Không mắc bệnh vẫn đạt Accuracy 91.5%. Bắt buộc phải kích hoạt class_weight='balanced', stratify khi chia tập và lấy Recall/ROC-AUC làm độ đo tối thượng."
    )


    code_feat_dist = '''# Vẽ Histogram cho toàn bộ các biến số học (Tuổi, BMI, Glucose...)
fig, axes = plt.subplots(3, 3, figsize=(15, 12))
for i, col in enumerate(numerical_cols):
    ax = axes[i // 3, i % 3]
    sns.histplot(df[col], kde=True, ax=ax, color='teal')
    ax.set_title(f'Phân bố của {col}')
plt.tight_layout()
plt.show()'''

    add_code_snippet_with_notes(
        doc,
        code_text=code_feat_dist,
        caption_text="Đoạn mã 7.5. Trực quan hóa phân bố các biến lâm sàng bằng vòng lặp.",
        description_items=[
            "Đoạn mã sử dụng vòng lặp for để tự động vẽ Histogram và đường KDE cho tất cả các biến số học.",
            "Cách tiếp cận này giúp tiết kiệm thời gian viết code lặp lại, đồng thời tạo ra mạng lưới biểu đồ tổng quan (Grid plot) được trình bày ở nhóm hình bên dưới."
        ],
        source_file="notebooks/01_diabetes.ipynb"
    )

    add_figure_with_notes(
        doc,
        "figures/diabetes/age_distribution.png",

        "Hình 7.2. Phân bố độ tuổi của bệnh nhân theo tình trạng bệnh.",
        [
            "Độ tuổi của nhóm mắc bệnh tiểu đường tập trung rất dày đặc ở khoảng 50 – 80 tuổi, với đỉnh phân bố quanh 60 tuổi.",
            "Ngược lại, nhóm không mắc bệnh phân bố đều từ trẻ em đến thanh thiếu niên và giảm dần ở tuổi già."
        ],
        explanation="Tuổi tác là yếu tố nguy cơ tự nhiên hàng đầu do sự suy giảm chức năng tuyến tụy và hiện tượng kháng insulin gia tăng theo thời gian.",
        ml_implication="Đặc trưng age mang trọng số tương quan dương mạnh mẽ, là thuộc tính phân tách ranh giới quan trọng hàng đầu trong các mô hình cây quyết định."
    )

    add_figure_with_notes(
        doc,
        "figures/diabetes/bmi_distribution.png",
        "Hình 7.3. Phân bố chỉ số khối cơ thể (BMI) của bệnh nhân.",
        [
            "Đa số bệnh nhân mắc tiểu đường có chỉ số BMI vượt ngưỡng 27 kg/m² (ngưỡng thừa cân và béo phì theo chuẩn WHO).",
            "Nhóm người bình thường có phân bố đỉnh BMI tập trung trong ngưỡng lý tưởng từ 20 – 25 kg/m²."
        ],
        explanation="Béo phì và mỡ nội tạng dư thừa giải phóng các chất trung gian gây viêm, làm suy giảm nghiêm trọng độ nhạy cảm của tế bào đối với insulin.",
        ml_implication="Do BMI có đuôi phân bố dài về phía bên phải (Right-skewed lên tới 90 kg/m²), việc áp dụng chuẩn hóa Z-score giúp kiểm soát ảnh hưởng của các giá trị cực biên đối với mô hình tuyến tính."
    )

    add_figure_with_notes(
        doc,
        "figures/diabetes/glucose_hba1c_distribution.png",
        "Hình 7.4. Phân bố nồng độ Glucose và HbA1c giữa hai nhóm bệnh nhân.",
        [
            "Có sự phân định cực kỳ rõ rệt giữa hai nhóm: Bệnh nhân tiểu đường có HbA1c vượt ngưỡng 6.5% và Glucose vượt 140 mg/dL.",
            "Ngược lại, người khỏe mạnh có HbA1c dưới 6.0% và Glucose dưới 120 mg/dL."
        ],
        explanation="HbA1c và Glucose là hai tiêu chuẩn vàng trong y khoa lâm sàng để chẩn đoán xác định bệnh tiểu đường.",
        ml_implication="Đây là cặp đặc trưng có khả năng phân tách tuyến tính mạnh nhất. Một lát cắt siêu phẳng trong không gian 2 chiều này đã có thể phân loại đúng hơn 85% mẫu bệnh."
    )


    code_corr = '''# Tính toán và vẽ Ma trận tương quan (Pearson Correlation)
plt.figure(figsize=(10, 8))
corr_matrix = df_clean[numerical_cols + [target_col]].corr()

sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="Blues")
plt.title("Ma trận tương quan Pearson giữa các biến lâm sàng")
plt.tight_layout()
plt.show()'''

    add_code_snippet_with_notes(
        doc,
        code_text=code_corr,
        caption_text="Đoạn mã 7.6. Tính toán ma trận tương quan Pearson.",
        description_items=[
            "Hàm .corr() của Pandas mặc định tính toán hệ số tương quan Pearson giữa các biến số.",
            "sns.heatmap hiển thị hệ số bằng màu sắc (Blues), giúp dễ dàng phát hiện mức độ phụ thuộc tuyến tính mạnh giữa 'glucose', 'HbA1c' với biến mục tiêu."
        ],
        source_file="notebooks/01_diabetes.ipynb"
    )

    add_figure_with_notes(
        doc,
        "figures/diabetes/correlation_heatmap.png",

        "Hình 7.5. Ma trận hệ số tương quan giữa các thuộc tính lâm sàng và biến mục tiêu.",
        [
            "Hai biến có hệ số tương quan Pearson cao nhất với nhãn diabetes là blood_glucose_level (r = 0.42) và HbA1c_level (r = 0.41).",
            "Các biến tuổi tác (r = 0.26) và BMI (r = 0.21) cũng có tương quan dương có ý nghĩa thống kê.",
            "Tương quan giữa các biến độc lập với nhau ở mức thấp (r < 0.3), không có hiện tượng đa cộng tuyến nghiêm trọng giữa các thuộc tính lâm sàng."
        ],
        explanation="Tín hiệu chẩn đoán tập trung chủ yếu ở hai chỉ số đường huyết, trong khi các thuộc tính nhân khẩu đóng vai trò điều kiện nguy cơ bổ trợ.",
        ml_implication="Mô hình tuyến tính và mô hình dựa trên cây đều có thể khai thác trực tiếp các thuộc tính này mà không lo ngại hiện tượng phân rã ma trận do đa cộng tuyến."
    )

    add_styled_heading(doc, "7.7. Xây dựng mô hình", 2)
    
    code_diab_train = '''model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', model)
])

# Huấn luyện toàn bộ Pipeline
pipeline.fit(X_train, y_train)

# Dự đoán và Đánh giá trên tập Validation
y_pred = pipeline.predict(X_val)
print(classification_report(y_val, y_pred))'''
    
    add_code_snippet_with_notes(
        doc,
        code_text=code_diab_train,
        caption_text="Đoạn mã 7.2. Huấn luyện và đánh giá mô hình phân loại.",
        description_items=[
            "Tích hợp tiền xử lý (preprocessor) và thuật toán (RandomForest) vào chung một Pipeline duy nhất.",
            "Tham số class_weight='balanced' được sử dụng để khắc phục tình trạng mất cân bằng nhãn (Imbalanced Data).",
            "Đoạn mã này sinh ra trực tiếp các chỉ số đánh giá Recall, F1-Score được trình bày trong bảng kết quả bên dưới."
        ],
        source_file="notebooks/01_diabetes.ipynb"
    )

    add_body_p(doc, "Tập dữ liệu sạch 96,146 mẫu được phân chia stratified thành: 67,302 mẫu Train (70%), 14,422 mẫu Validation (15%) và 14,422 mẫu Test (15%). Mô hình Baseline DummyClassifier được đưa vào đối đầu trực tiếp cùng 5 thuật toán học máy phân lớp phổ biến.")

    add_styled_heading(doc, "7.8. Đánh giá mô hình", 2)
    add_styled_table(
        doc,
        "Bảng 7.2. So sánh hiệu năng các mô hình phân loại bệnh tiểu đường trên tập Validation",
        ["Mô hình", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC", "Thời gian (s)"],
        [
            ["Dummy Baseline", "0.8400", "0.0876", "0.0865", "0.0871", "0.4997", "0.05s"],
            ["Logistic Regression", "0.8850", "0.4271", "0.8892", "0.5770", "0.9624", "0.65s"],
            ["KNN (k=5)", "0.9575", "0.8601", "0.6187", "0.7197", "0.9074", "0.16s"],
            ["Decision Tree", "0.8315", "0.3387", "0.9560", "0.5002", "0.9677", "0.11s"],
            ["Random Forest", "0.9022", "0.4719", "0.9167", "0.6230", "0.9757", "0.94s"],
            ["SVM (LinearSVC)", "0.9570", "0.8446", "0.6281", "0.7205", "0.9624", "1.79s"]
        ],
        col_widths=[1.6, 0.8, 0.8, 0.8, 0.8, 0.8, 1.0],
        align_cols=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER]
    )


    code_model_comp = '''# Vẽ biểu đồ so sánh hiệu năng các mô hình
df_metrics = pd.DataFrame(results).T

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
colors = ['#4e79a7', '#f28e2c', '#e15759', '#76b7b2']

for idx, metric in enumerate(metrics):
    ax = axes[idx // 2, idx % 2]
    df_metrics[metric].plot(kind='bar', ax=ax, color=colors[idx])
    ax.set_title(f'So sánh {metric}')
    ax.set_ylim(0, 1)

plt.tight_layout()
plt.show()'''

    add_code_snippet_with_notes(
        doc,
        code_text=code_model_comp,
        caption_text="Đoạn mã 7.7. Trực quan hóa kết quả so sánh các mô hình học máy.",
        description_items=[
            "Các chỉ số Accuracy, Precision, Recall và F1-Score của 5 mô hình được lưu vào một pandas DataFrame.",
            "Vòng lặp tự động gọi hàm .plot(kind='bar') để so sánh trực quan hiệu năng, cho phép người đọc nhận thấy sự vượt trội về Recall của Random Forest ở nhóm hình bên dưới."
        ],
        source_file="notebooks/01_diabetes.ipynb"
    )

    add_figure_with_notes(
        doc,
        "figures/diabetes/model_comparison.png",

        "Hình 7.6. Biểu đồ so sánh hiệu năng các mô hình phân loại bệnh tiểu đường trên tập Validation.",
        [
            "Mô hình Random Forest và Decision Tree áp đảo hoàn toàn về chỉ số Recall (>91%), vượt trội so với KNN và SVM vốn chỉ đạt Recall quanh 62%.",
            "Về tổng thể diện tích dưới đường cong ROC-AUC, Random Forest dẫn đầu toàn diện với chỉ số đạt 0.9757."
        ],
        explanation="KNN và SVM bị ảnh hưởng tiêu cực bởi mất cân bằng nhãn khi lề phân tách bị kéo lệch về phía lớp đa số, trong khi Random Forest áp dụng cân bằng trọng số (balanced) học được ranh giới bao phủ toàn bộ lớp thiểu số.",
        ml_implication="Khẳng định tầm quan trọng của việc điều chỉnh trọng số lớp trong bài toán chẩn đoán y tế."
    )


    code_cm = '''cm = confusion_matrix(y_test, y_test_pred)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Dự đoán: Không mắc", "Dự đoán: Mắc bệnh"],
            yticklabels=["Thực tế: Không mắc", "Thực tế: Mắc bệnh"])
plt.title("Confusion Matrix trên Test Set — Random Forest")
plt.tight_layout()
plt.show()'''
    add_code_snippet_with_notes(
        doc,
        code_text=code_cm,
        caption_text="Đoạn mã 7.3. Trực quan hóa Ma trận nhầm lẫn (Confusion Matrix).",
        description_items=[
            "Sử dụng thư viện Seaborn để vẽ ma trận nhiệt hiển thị kết quả phân loại.",
            "Làm rõ số lượng dự đoán đúng/sai cho từng nhãn cụ thể, từ đó phân tích sâu về False Positives và False Negatives."
        ],
        source_file="notebooks/01_diabetes.ipynb"
    )

    add_figure_with_notes(
        doc,
        "figures/diabetes/confusion_matrix.png",

        "Hình 7.7. Ma trận nhầm lẫn (Confusion Matrix) của mô hình Random Forest trên tập Test độc lập.",
        [
            "Trên tổng số 14,422 bệnh nhân kiểm thử độc lập, mô hình phát hiện chính xác 1,141 ca mắc bệnh thực sự (True Positives).",
            "Số ca mắc bệnh bị bỏ sót (False Negatives) chỉ là 131 ca trên toàn bộ 1,272 ca bệnh thực tế, mang lại độ nhạy chẩn đoán Recall = 89.70%.",
            "Số ca không mắc bệnh bị cảnh báo nhầm (False Positives) là 1,339 ca (chiếm ~10% tổng ca khỏe mạnh)."
        ],
        explanation="Trong y tế dự phòng, chi phí của một ca False Negative là khôn lường: bệnh nhân không biết mình mắc bệnh sẽ không được điều trị, dẫn tới biến chứng suy thận hoặc đột quỵ. Ngược lại, chi phí của một ca False Positive chỉ là một xét nghiệm khẳng định đường huyết lại.",
        ml_implication="Đánh đổi một lượng nhỏ Precision để đạt Recall xấp xỉ 90% là chiến lược y khoa tối ưu nhất."
    )

    add_styled_heading(doc, "7.9. Phân tích lỗi trên tập Test (Error Analysis)", 2)
    add_body_p(doc, "Phân tích chi tiết 1,470 ca dự đoán sai trên tập Test:")
    add_bullet_p(doc, "Chiếm 131 ca. Phần lớn các ca này xảy ra ở những bệnh nhân trẻ tuổi có nồng độ glucose và HbA1c ở ngưỡng chớm vượt ngưỡng bình thường (tiền tiểu đường), khiến mô hình chưa đủ tín hiệu vượt ngưỡng kích hoạt. Cần bổ sung xét nghiệm dung nạp glucose đường uống (OGTT) đối với nhóm nghi ngờ này.", bold_prefix="Ca bệnh bị bỏ sót (False Negative = 131): ")
    add_bullet_p(doc, "Chiếm 1,339 ca. Tập trung ở người cao tuổi có chỉ số BMI cao nhưng nồng độ đường huyết vẫn duy trì ở ngưỡng an toàn nhờ chế độ ăn kiêng. Mô hình có xu hướng cảnh báo thận trọng dựa trên yếu tố tuổi tác và béo phì.", bold_prefix="Cảnh báo nhầm (False Positive = 1,339): ")

    add_styled_heading(doc, "7.10. Lựa chọn mô hình chính thức", 2)
    add_body_p(doc, "Mô hình Random Forest Classifier với tham số class_weight='balanced' được lựa chọn chính thức để đóng gói và triển khai. Bảng kết quả kiểm định cuối cùng trên tập Test 14,422 mẫu độc lập:")
    add_styled_table(
        doc,
        "Bảng 7.3. Kết quả kiểm định mô hình Random Forest trên tập Test độc lập",
        ["Chỉ số đánh giá", "Giá trị thực nghiệm", "Đánh giá chuyên môn"],
        [
            ["Accuracy", "0.8981 (89.81%)", "Độ chính xác tổng quan ở mức rất cao"],
            ["Precision", "0.4601 (46.01%)", "Chấp nhận mức cảnh báo rộng để bao phủ tối đa"],
            ["Recall (Sensitivity)", "0.8970 (89.70%)", "Bắt trúng gần 9/10 ca bệnh thực tế trong cộng đồng"],
            ["F1-Score", "0.6082", "Cân bằng hài hòa giữa độ chính xác và độ nhạy"],
            ["ROC-AUC", "0.9743", "Năng lực phân định nhãn ở mức xuất sắc vượt trội"]
        ],
        col_widths=[2.0, 1.8, 2.8]
    )

    add_styled_heading(doc, "7.11. Triển khai hệ thống", 2)

    add_figure_with_notes(
        doc,
        "screenshots/api/api_diabetes_result.png",
        "Hình 7.8. Kết quả gọi API dự đoán bệnh tiểu đường (/predict/diabetes) trên giao diện Swagger UI.",
        [
            "Request gửi lên gồm các chỉ số: age=45, bmi=28.5, HbA1c=6.8, glucose=155, smoking=never, gender=Male.",
            "Mô hình phản hồi tức thời: prediction=1 (Cảnh báo nguy cơ tiểu đường), xác suất mắc bệnh 86.4%, mức độ rủi ro 'High Risk'."
        ],
        explanation="Pipeline tự động chuẩn hóa dữ liệu đầu vào và chuyển qua Random Forest để xuất ra xác suất hậu nghiệm qua predict_proba.",
        ml_implication="API cung cấp đầy đủ thông tin định lượng giúp y bác sĩ tham vấn kết quả nhanh chóng."
    )

    add_figure_with_notes(
        doc,
        "screenshots/web/diabetes_web_result.png",
        "Hình 7.9. Kết quả chẩn đoán nguy cơ tiểu đường trên giao diện Web Desktop.",
        [
            "Giao diện trực quan hóa kết quả dưới dạng thẻ cảnh báo màu đỏ nổi bật (High Risk) kèm theo thanh đo phần trăm xác suất sinh động.",
            "Hệ thống tự động hiển thị khuyến nghị y tế: Đề xuất bệnh nhân đến cơ sở chuyên khoa nội tiết để xét nghiệm khẳng định."
        ],
        explanation="Trực quan hóa trực tiếp từ dữ liệu JSON trả về bởi API.",
        ml_implication="Giúp người dùng không chuyên về kỹ thuật có thể hiểu ngay tình trạng sức khỏe cá nhân."
    )

    add_figure_with_notes(
        doc,
        "screenshots/mobile/diabetes_mobile.png",
        "Hình 7.10. Giao diện chẩn đoán tiểu đường trên thiết bị di động truy cập qua mạng LAN (Smartphone Viewport).",
        [
            "Giao diện co giãn chuẩn xác trên màn hình điện thoại di động, các trường nhập liệu lâm sàng được sắp xếp gọn gàng theo chiều dọc.",
            "Kết quả chẩn đoán hiển thị mượt mà không có hiện tượng giật lag hay vỡ giao diện."
        ],
        explanation="Hoạt động hoàn hảo trên trình duyệt điện thoại kết nối qua Wi-Fi mạng LAN.",
        ml_implication="Cho phép nhân viên y tế cộng đồng có thể cầm smartphone đi thu thập và sàng lọc sức khỏe trực tiếp tại vùng sâu vùng xa.",
        max_width_inches=3.2
    )
