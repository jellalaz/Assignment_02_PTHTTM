import re

with open("scripts/report_builder/ch9_ecommerce.py", "r", encoding="utf-8") as f:
    content = f.read()

# Make sure we import add_code_snippet_with_notes
if "add_code_snippet_with_notes" not in content:
    content = content.replace(
        "add_styled_heading, add_body_p, add_bullet_p, add_code_block,",
        "add_styled_heading, add_body_p, add_bullet_p, add_code_block, add_code_snippet_with_notes,"
    )

# Snippet 1 insertion
snippet_1 = """    add_styled_heading(doc, "9.4. Biểu diễn dữ liệu đa phương thức", 2)
    
    code_ecom_preprocess = '''# Khối xử lý ngôn ngữ tự nhiên (NLP)
text_transformer = Pipeline(steps=[
    ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2)))
])

# Khối xử lý dữ liệu cấu trúc (Tabular)
tabular_transformer = ColumnTransformer(transformers=[
    ('num', StandardScaler(), num_cols),
    ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), cat_cols)
])

# Gộp chung cả 2 khối thành một Pipeline duy nhất
combined_features = ColumnTransformer(transformers=[
    ('text', text_transformer, 'Review Text'),
    ('tabular', tabular_transformer, tabular_cols)
])'''
    add_code_snippet_with_notes(
        doc,
        code_text=code_ecom_preprocess,
        caption_text="Đoạn mã 9.1. Biểu diễn dữ liệu đa phương thức (Văn bản + Bảng).",
        description_items=[
            "Chuyển đổi văn bản đánh giá thành không gian vector bằng thuật toán TF-IDF (hỗ trợ n-gram từ 1 đến 2 từ).",
            "Xử lý song song dữ liệu dạng bảng và gộp chung (Combined) để tạo ra tập đặc trưng hoàn chỉnh nhằm tận dụng tối đa thông tin từ mọi luồng dữ liệu."
        ],
        source_file="src/ecommerce/pipeline.py"
    )
"""
content = content.replace('    add_styled_heading(doc, "9.4. Biểu diễn dữ liệu đa phương thức", 2)', snippet_1)

# Snippet 2 insertion
snippet_2 = """    add_styled_heading(doc, "9.5. Xây dựng mô hình", 2)
    
    code_ecom_train = '''model = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)

pipeline = Pipeline(steps=[
    ('preprocessor', combined_features),
    ('classifier', model)
])

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_val)
print("Accuracy:", accuracy_score(y_val, y_pred))'''
    
    add_code_snippet_with_notes(
        doc,
        code_text=code_ecom_train,
        caption_text="Đoạn mã 9.2. Huấn luyện mô hình hồi quy logistic trên tập đặc trưng kết hợp.",
        description_items=[
            "Đoạn mã khởi tạo Pipeline chứa cả bộ tiền xử lý đa phương thức và thuật toán Logistic Regression.",
            "Việc sử dụng Logistic Regression giúp đảm bảo tốc độ huấn luyện cực nhanh trên ma trận thưa TF-IDF khổng lồ (Sparse Matrix) mà không bị bùng nổ bộ nhớ.",
            "Sự kết hợp này trực tiếp đem lại độ chính xác đạt >93% như trình bày ở Bảng 9.2."
        ],
        source_file="notebooks/03_ecommerce.ipynb"
    )
"""
content = content.replace('    add_styled_heading(doc, "9.5. Xây dựng mô hình", 2)', snippet_2)

with open("scripts/report_builder/ch9_ecommerce.py", "w", encoding="utf-8") as f:
    f.write(content)
