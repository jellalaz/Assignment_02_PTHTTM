import re

with open("scripts/report_builder/ch9_ecommerce.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Target / Rating Distribution
snippet_rating = """
    code_ecom_rating = '''# Trực quan hóa Biến mục tiêu (Recommended IND) và Điểm đánh giá (Rating)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Phân bố Recommended IND
sns.countplot(x='Recommended IND', data=df, ax=axes[0], palette='pastel')
axes[0].set_title('Phân bố Khuyên dùng (Recommended IND)')

# Phân bố Rating
sns.countplot(x='Rating', data=df, ax=axes[1], palette='viridis')
axes[1].set_title('Phân bố Điểm đánh giá (Rating)')

plt.tight_layout()
plt.show()'''

    add_code_snippet_with_notes(
        doc,
        code_text=code_ecom_rating,
        caption_text="Đoạn mã 9.4. Khảo sát phân bố của Biến mục tiêu và Biến đánh giá (Rating).",
        description_items=[
            "Sử dụng biểu đồ Countplot để thống kê sự chênh lệch nhãn của biến phân loại (Recommended IND).",
            "Đồng thời kiểm tra sự liên hệ mật thiết giữa điểm Rating (từ 1 đến 5 sao) và nhãn khuyên dùng."
        ],
        source_file="notebooks/03_ecommerce.ipynb"
    )

    add_figure_with_notes(
        doc,
        "figures/ecommerce/target_rating_distribution.png",
"""
content = content.replace('    add_figure_with_notes(\n        doc,\n        "figures/ecommerce/target_rating_distribution.png",', snippet_rating)

# 2. Review Length Boxplot
snippet_length = """
    code_ecom_len = '''# Tính toán và trực quan hóa chiều dài bình luận theo Phòng ban
df['Review Length'] = df['Review Text'].astype(str).apply(len)

plt.figure(figsize=(12, 6))
sns.boxplot(x='Department Name', y='Review Length', data=df, palette='Set3')
plt.title("Phân bố Chiều dài Bình luận theo từng Phòng ban (Department)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()'''

    add_code_snippet_with_notes(
        doc,
        code_text=code_ecom_len,
        caption_text="Đoạn mã 9.5. Tính toán chiều dài văn bản và vẽ biểu đồ Boxplot.",
        description_items=[
            "Sử dụng hàm apply(len) trên cột pandas để trích xuất nhanh số lượng ký tự của mỗi bình luận.",
            "Biểu đồ Boxplot giúp dễ dàng nhận ra giá trị ngoại lai (outliers) và sự khác biệt về độ dài đánh giá giữa các phòng ban."
        ],
        source_file="notebooks/03_ecommerce.ipynb"
    )

    add_figure_with_notes(
        doc,
        "figures/ecommerce/department_review_length.png",
"""
content = content.replace('    add_figure_with_notes(\n        doc,\n        "figures/ecommerce/department_review_length.png",', snippet_length)


# 3. Representation Comparison
snippet_rep = """
    code_ecom_rep = '''# Vẽ biểu đồ Barplot so sánh 3 phương pháp biểu diễn dữ liệu
plt.figure(figsize=(10, 6))
sns.barplot(
    x='Representation', 
    y='Accuracy', 
    data=df_comparison, 
    palette='magma'
)

plt.title("So sánh Hiệu năng (Accuracy) theo Phương pháp Biểu diễn Dữ liệu")
plt.ylim(0.8, 1.0)
plt.axhline(y=0.9320, color='r', linestyle='--')
plt.tight_layout()
plt.show()'''

    add_code_snippet_with_notes(
        doc,
        code_text=code_ecom_rep,
        caption_text="Đoạn mã 9.6. So sánh hiệu năng giữa phương pháp Tabular, Text và Combined.",
        description_items=[
            "Đoạn mã trực quan hóa DataFrame chứa kết quả Accuracy của 3 phương pháp huấn luyện.",
            "Đường nét đứt màu đỏ (axhline) được chèn thêm để làm nổi bật mốc hiệu năng xuất sắc nhất (>93%) đạt được khi kết hợp cả dữ liệu dạng bảng và văn bản."
        ],
        source_file="notebooks/03_ecommerce.ipynb"
    )

    add_figure_with_notes(
        doc,
        "figures/ecommerce/representation_comparison.png",
"""
content = content.replace('    add_figure_with_notes(\n        doc,\n        "figures/ecommerce/representation_comparison.png",', snippet_rep)


# 4. Confusion Matrix
snippet_cm = """
    code_ecom_cm = '''# Trực quan hóa Ma trận nhầm lẫn cho Text Classification
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Greens",
            xticklabels=["Not Recommended", "Recommended"],
            yticklabels=["Not Recommended", "Recommended"])

plt.title("Confusion Matrix (Combined Features - Logistic Regression)")
plt.tight_layout()
plt.show()'''

    add_code_snippet_with_notes(
        doc,
        code_text=code_ecom_cm,
        caption_text="Đoạn mã 9.7. Ma trận nhầm lẫn (Confusion Matrix) trên tập Test độc lập.",
        description_items=[
            "Đoạn mã kiểm định năng lực mô hình Logistic Regression trên tập đặc trưng kết hợp.",
            "Ma trận nhiệt (Heatmap) giúp đánh giá trực quan tỷ lệ nhận diện sai lệch các đánh giá tiêu cực (Not Recommended)."
        ],
        source_file="notebooks/03_ecommerce.ipynb"
    )

    add_figure_with_notes(
        doc,
        "figures/ecommerce/confusion_matrix.png",
"""
content = content.replace('    add_figure_with_notes(\n        doc,\n        "figures/ecommerce/confusion_matrix.png",', snippet_cm)

with open("scripts/report_builder/ch9_ecommerce.py", "w", encoding="utf-8") as f:
    f.write(content)
