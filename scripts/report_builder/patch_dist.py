import re

# 1. DIABETES TARGET DISTRIBUTION
with open("scripts/report_builder/ch7_diabetes.py", "r", encoding="utf-8") as f:
    content = f.read()

snippet_diab_dist = """
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
"""
content = content.replace('    add_figure_with_notes(\n        doc,\n        "figures/diabetes/target_distribution.png",', snippet_diab_dist)

with open("scripts/report_builder/ch7_diabetes.py", "w", encoding="utf-8") as f:
    f.write(content)


# 2. HOUSE PRICE DISTRIBUTION
with open("scripts/report_builder/ch8_house.py", "r", encoding="utf-8") as f:
    content = f.read()

snippet_house_dist = """
    code_house_dist = '''# Vẽ phân bố giá bán (Histogram + KDE)
plt.figure(figsize=(8, 5))
sns.histplot(df['Price'], bins=50, kde=True, color='skyblue')
plt.title("Phân bố Giá bán Bất động sản (House Price Distribution)")
plt.xlabel("Giá bán")
plt.ylabel("Tần suất")
plt.tight_layout()
plt.show()'''

    add_code_snippet_with_notes(
        doc,
        code_text=code_house_dist,
        caption_text="Đoạn mã 8.3. Trực quan hóa phân bố biến liên tục bằng Histogram và đường KDE.",
        description_items=[
            "Sử dụng sns.histplot kết hợp tham số kde=True để vẽ biểu đồ phân bố tần suất và đường cong mật độ ước lượng.",
            "Đoạn mã giúp phát hiện hiện tượng phân bố lệch phải (Right-skewed) của giá nhà, từ đó hiểu rõ hơn về đặc tính dữ liệu thị trường thực tế."
        ],
        source_file="notebooks/02_house_price.ipynb"
    )

    add_figure_with_notes(
        doc,
        "figures/house_price/price_distribution.png",
"""
content = content.replace('    add_figure_with_notes(\n        doc,\n        "figures/house_price/price_distribution.png",', snippet_house_dist)

with open("scripts/report_builder/ch8_house.py", "w", encoding="utf-8") as f:
    f.write(content)


# 3. E-COMMERCE TOP KEYWORDS
with open("scripts/report_builder/ch9_ecommerce.py", "r", encoding="utf-8") as f:
    content = f.read()

snippet_ecom_dist = """
    code_ecom_kw = '''# Lấy danh sách từ vựng và tần suất (Top Keywords)
feature_names = tfidf_vectorizer.get_feature_names_out()
sums = X_tfidf.sum(axis=0)

# Chuyển đổi thành DataFrame và sắp xếp
data = []
for col, term in enumerate(feature_names):
    data.append( (term, sums[0, col]) )
ranking = pd.DataFrame(data, columns=['term','rank'])
top_keywords = ranking.sort_values('rank', ascending=False).head(20)

# Vẽ biểu đồ Barplot
plt.figure(figsize=(10, 6))
sns.barplot(x='rank', y='term', data=top_keywords, palette='viridis')
plt.title("Top 20 cụm từ xuất hiện nhiều nhất (TF-IDF Weight)")
plt.tight_layout()
plt.show()'''

    add_code_snippet_with_notes(
        doc,
        code_text=code_ecom_kw,
        caption_text="Đoạn mã 9.3. Khai thác và trực quan hóa Top 20 từ khóa từ ma trận TF-IDF.",
        description_items=[
            "Sử dụng hàm get_feature_names_out() để trích xuất các từ vựng sau khi xử lý ngôn ngữ tự nhiên.",
            "Tính tổng trọng số TF-IDF của từng từ khóa trên toàn bộ kho văn bản và dùng sns.barplot để trực quan hóa những từ mang tính quyết định nhất (như 'love', 'great', 'perfect')."
        ],
        source_file="notebooks/03_ecommerce.ipynb"
    )

    add_figure_with_notes(
        doc,
        "figures/ecommerce/top_keywords_tfidf.png",
"""
content = content.replace('    add_figure_with_notes(\n        doc,\n        "figures/ecommerce/top_keywords_tfidf.png",', snippet_ecom_dist)

with open("scripts/report_builder/ch9_ecommerce.py", "w", encoding="utf-8") as f:
    f.write(content)
