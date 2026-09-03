import re

# 1. DIABETES CONFUSION MATRIX
with open("scripts/report_builder/ch7_diabetes.py", "r", encoding="utf-8") as f:
    content = f.read()

snippet_cm = """
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
"""
content = content.replace('    add_figure_with_notes(\n        doc,\n        "figures/diabetes/confusion_matrix.png",', snippet_cm)

with open("scripts/report_builder/ch7_diabetes.py", "w", encoding="utf-8") as f:
    f.write(content)

# 2. WEB FRONTEND FETCH
with open("scripts/report_builder/ch6_deployment_methods.py", "r", encoding="utf-8") as f:
    content = f.read()

snippet_web = """
    code_web = '''// Gửi dữ liệu bệnh nhân từ Form HTML lên máy chủ
const payload = {
  gender: document.getElementById('dia-gender').value,
  age: parseFloat(document.getElementById('dia-age').value),
  bmi: parseFloat(document.getElementById('dia-bmi').value),
  // ... các chỉ số lâm sàng khác ...
};

// Gọi REST API bất đồng bộ bằng Fetch API
const res = await fetch('/predict/diabetes', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(payload)
});

const data = await res.json();
displayDiabetesResult(data);  // Cập nhật giao diện với xác suất trả về'''

    add_code_snippet_with_notes(
        doc,
        code_text=code_web,
        caption_text="Đoạn mã 6.3. Gọi REST API từ giao diện Client (JavaScript).",
        description_items=[
            "Đóng gói dữ liệu người dùng nhập thành định dạng JSON.",
            "Sử dụng Fetch API bất đồng bộ để gọi máy chủ dự đoán và lấy kết quả mà không cần tải lại trang.",
            "Tương thích hoàn toàn khi triển khai public hoặc mạng nội bộ LAN."
        ],
        source_file="web/static/js/app.js"
    )

    add_figure_with_notes(
        doc,
        "screenshots/web/web_home.png",
"""
content = content.replace('    add_figure_with_notes(\n        doc,\n        "screenshots/web/web_home.png",', snippet_web)

with open("scripts/report_builder/ch6_deployment_methods.py", "w", encoding="utf-8") as f:
    f.write(content)
