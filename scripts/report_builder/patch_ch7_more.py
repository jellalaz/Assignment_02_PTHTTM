import re

with open("scripts/report_builder/ch7_diabetes.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Feature Distribution (Before age_distribution.png)
snippet_feat_dist = """
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
"""
content = content.replace('    add_figure_with_notes(\n        doc,\n        "figures/diabetes/age_distribution.png",', snippet_feat_dist)

# 2. Correlation heatmap (Before correlation_heatmap.png)
snippet_corr = """
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
"""
content = content.replace('    add_figure_with_notes(\n        doc,\n        "figures/diabetes/correlation_heatmap.png",', snippet_corr)


# 3. Model Comparison (Before model_comparison.png)
snippet_model_comp = """
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
"""
content = content.replace('    add_figure_with_notes(\n        doc,\n        "figures/diabetes/model_comparison.png",', snippet_model_comp)


with open("scripts/report_builder/ch7_diabetes.py", "w", encoding="utf-8") as f:
    f.write(content)
