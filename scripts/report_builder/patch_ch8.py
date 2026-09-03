import re

with open("scripts/report_builder/ch8_house.py", "r", encoding="utf-8") as f:
    content = f.read()

# Make sure we import add_code_snippet_with_notes
if "add_code_snippet_with_notes" not in content:
    content = content.replace(
        "add_styled_heading, add_body_p, add_bullet_p, add_code_block,",
        "add_styled_heading, add_body_p, add_bullet_p, add_code_block, add_code_snippet_with_notes,"
    )

# Snippet 1 insertion
snippet_1 = """    add_styled_heading(doc, "8.4. Tiền xử lý dữ liệu và trích xuất đặc trưng", 2)
    add_body_p(doc, "Dữ liệu được chuyển đổi thành các vector số học trước khi đưa vào mô hình học máy:")
    
    code_house_preprocess = '''# Tách biến mục tiêu (Price) và các biến đặc trưng
X = df.drop(columns=['Price'])
y = df['Price']

preprocessor = ColumnTransformer(transformers=[
    ('num', StandardScaler(), num_cols),
    ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), cat_cols)
])'''
    add_code_snippet_with_notes(
        doc,
        code_text=code_house_preprocess,
        caption_text="Đoạn mã 8.1. Phân tách đặc trưng và khởi tạo bộ tiền xử lý.",
        description_items=[
            "Tách riêng cột mục tiêu 'Price' khỏi tập dữ liệu.",
            "Chuẩn hóa dữ liệu tương tự như bài toán tiểu đường, tập trung xử lý hiện tượng đa cộng tuyến bằng tham số drop='first' trong OneHotEncoder."
        ],
        source_file="src/house_price/pipeline.py"
    )
"""
content = content.replace('    add_styled_heading(doc, "8.4. Tiền xử lý dữ liệu và trích xuất đặc trưng", 2)', snippet_1)

# Snippet 2 insertion
snippet_2 = """    add_styled_heading(doc, "8.5. Xây dựng mô hình", 2)
    
    code_house_train = '''best_model = GradientBoostingRegressor(
    n_estimators=200, 
    learning_rate=0.1, 
    random_state=42
)

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', best_model)
])

pipeline.fit(X_train, y_train)

# Đánh giá độ lỗi MAE và hệ số xác định R2
y_pred = pipeline.predict(X_val)
print("MAE:", mean_absolute_error(y_val, y_pred))
print("R2 Score:", r2_score(y_val, y_pred))'''
    
    add_code_snippet_with_notes(
        doc,
        code_text=code_house_train,
        caption_text="Đoạn mã 8.2. Huấn luyện thuật toán Gradient Boosting cho bài toán hồi quy.",
        description_items=[
            "Khởi tạo thuật toán Gradient Boosting với 200 cây quyết định (estimators).",
            "Mô hình được huấn luyện toàn trình (End-to-end) thông qua Pipeline.",
            "Các chỉ số đánh giá độ lỗi (MAE) và độ khớp (R2) sinh ra từ đoạn mã này được tổng hợp chi tiết tại Bảng 8.3."
        ],
        source_file="notebooks/02_house_price.ipynb"
    )
"""
content = content.replace('    add_styled_heading(doc, "8.5. Xây dựng mô hình", 2)', snippet_2)

with open("scripts/report_builder/ch8_house.py", "w", encoding="utf-8") as f:
    f.write(content)
