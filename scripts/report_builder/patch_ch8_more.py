import re

with open("scripts/report_builder/ch8_house.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Correlation heatmap (Before correlation_heatmap.png)
snippet_corr = """
    code_house_corr = '''# Ma trận tương quan các đặc trưng số học với Giá nhà
plt.figure(figsize=(10, 8))
corr_matrix = df[['Price', 'Area', 'Bedrooms', 'Bathrooms', 'Stories', 'Parking']].corr()

sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Mức độ tương quan (Pearson) giữa Giá nhà và các đặc trưng")
plt.tight_layout()
plt.show()'''

    add_code_snippet_with_notes(
        doc,
        code_text=code_house_corr,
        caption_text="Đoạn mã 8.4. Tính toán và trực quan hóa tương quan tuyến tính.",
        description_items=[
            "Đoạn mã lọc ra các biến số học cốt lõi như Diện tích (Area), Số phòng ngủ (Bedrooms) để đo lường mức độ tác động lên Giá nhà.",
            "Bản đồ nhiệt (Heatmap) giúp dễ dàng nhận định Diện tích (Area) là yếu tố quyết định lớn nhất đối với sự thay đổi của giá bán."
        ],
        source_file="notebooks/02_house_price.ipynb"
    )

    add_figure_with_notes(
        doc,
        "figures/house_price/correlation_heatmap.png",
"""
content = content.replace('    add_figure_with_notes(\n        doc,\n        "figures/house_price/correlation_heatmap.png",', snippet_corr)

# 2. Model Comparison (Before model_comparison.png)
snippet_model_comp = """
    code_house_model = '''# So sánh MAE và R2 Score giữa các mô hình
df_metrics = pd.DataFrame(results).T

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Biểu đồ MAE (Càng thấp càng tốt)
df_metrics['MAE'].sort_values().plot(kind='bar', color='salmon', ax=axes[0])
axes[0].set_title('So sánh Mean Absolute Error (MAE)')

# Biểu đồ R2 (Càng cao càng tốt)
df_metrics['R2 Score'].sort_values(ascending=False).plot(kind='bar', color='skyblue', ax=axes[1])
axes[1].set_title('So sánh R2 Score (Độ khớp)')

plt.tight_layout()
plt.show()'''

    add_code_snippet_with_notes(
        doc,
        code_text=code_house_model,
        caption_text="Đoạn mã 8.5. Trực quan hóa độ lỗi (MAE) và độ khớp (R2 Score).",
        description_items=[
            "Chuyển đổi kết quả đánh giá (dictionary) thành Pandas DataFrame để vẽ biểu đồ so sánh song song.",
            "Biểu đồ trực quan hóa MAE (Sắp xếp tăng dần) và R2 (Sắp xếp giảm dần) giúp khẳng định Gradient Boosting là mô hình tối ưu nhất trong bảng xếp hạng."
        ],
        source_file="notebooks/02_house_price.ipynb"
    )

    add_figure_with_notes(
        doc,
        "figures/house_price/model_comparison.png",
"""
content = content.replace('    add_figure_with_notes(\n        doc,\n        "figures/house_price/model_comparison.png",', snippet_model_comp)

# 3. Residual Plot / Actual vs Predicted (Before actual_vs_predicted_residuals.png)
snippet_res = """
    code_house_res = '''# Đánh giá phần dư (Residuals) của mô hình Gradient Boosting
residuals = y_test - y_pred_gb

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Biểu đồ Giá thực tế vs Giá dự đoán
sns.scatterplot(x=y_test, y=y_pred_gb, alpha=0.5, ax=axes[0])
axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
axes[0].set_title('Giá thực tế vs Giá dự đoán')

# Biểu đồ phân bố phần dư
sns.histplot(residuals, kde=True, ax=axes[1], color='purple')
axes[1].set_title('Phân bố phần dư (Residuals)')

plt.tight_layout()
plt.show()'''

    add_code_snippet_with_notes(
        doc,
        code_text=code_house_res,
        caption_text="Đoạn mã 8.6. Trực quan hóa phần dư (Residual Analysis).",
        description_items=[
            "Tính toán giá trị sai số phần dư (Giá trị thực tế trừ đi Giá trị dự đoán).",
            "Đoạn mã sinh ra biểu đồ Scatter plot (Kiểm tra độ bám sát đường chéo lý tưởng) và Histogram (Kiểm tra phần dư có tuân theo phân bố chuẩn hóa hay không)."
        ],
        source_file="notebooks/02_house_price.ipynb"
    )

    add_figure_with_notes(
        doc,
        "figures/house_price/actual_vs_predicted_residuals.png",
"""
content = content.replace('    add_figure_with_notes(\n        doc,\n        "figures/house_price/actual_vs_predicted_residuals.png",', snippet_res)

with open("scripts/report_builder/ch8_house.py", "w", encoding="utf-8") as f:
    f.write(content)
