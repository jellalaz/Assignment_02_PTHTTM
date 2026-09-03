import re

with open("scripts/report_builder/ch7_diabetes.py", "r", encoding="utf-8") as f:
    content = f.read()

# Make sure we import add_code_snippet_with_notes
if "add_code_snippet_with_notes" not in content:
    content = content.replace(
        "add_styled_heading, add_body_p, add_bullet_p, add_code_block,",
        "add_styled_heading, add_body_p, add_bullet_p, add_code_block, add_code_snippet_with_notes,"
    )

# Snippet 1 insertion
snippet_1 = """    add_styled_heading(doc, "7.5. Biểu diễn dữ liệu", 2)
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
"""
content = content.replace('    add_styled_heading(doc, "7.5. Biểu diễn dữ liệu", 2)', snippet_1)

# Snippet 2 insertion
snippet_2 = """    add_styled_heading(doc, "7.7. Xây dựng mô hình", 2)
    
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
"""
content = content.replace('    add_styled_heading(doc, "7.7. Xây dựng mô hình", 2)', snippet_2)

with open("scripts/report_builder/ch7_diabetes.py", "w", encoding="utf-8") as f:
    f.write(content)
