# SCREENSHOTS CATALOG & EVIDENCE MAPPING

Tất cả các ảnh chụp trong thư mục này được sinh ra từ **hệ thống thật đang chạy** (FastAPI backend + Google Chrome headless automation), tuyệt đối **không sử dụng ảnh mẫu hay dữ liệu giả lập**.

---

## 1. Desktop Web Application (`screenshots/web/`)

| Tên Tệp | Khung nhìn | Nội dung thể hiện | Đưa vào mục báo cáo |
|---|---|---|---|
| `web_home.png` | 1280 × 900 | Màn hình giao diện Desktop tổng thể, thanh điều hướng tab, form nhập liệu mẫu | Chương 6: Triển khai Web (Giao diện tổng quan) |
| `diabetes_web_result.png` | 1280 × 900 | Kết quả dự đoán Tiểu đường (Probability gauge 93.7%, nhãn Diabetic High Risk) | Chương 6: Triển khai ứng dụng Tiểu đường |
| `house_web_result.png` | 1280 × 900 | Kết quả định giá nhà thực tế ($1,768,153.91 dựa trên mô hình Ridge Regression) | Chương 6: Triển khai ứng dụng Giá nhà |
| `ecommerce_web_result.png` | 1280 × 900 | Kết quả phân tích đánh giá (Confidence 99.0%, Recommended Positive) | Chương 6: Triển khai ứng dụng E-Commerce |

---

## 2. Responsive Mobile Web Client (`screenshots/mobile/`)

| Tên Tệp | Khung nhìn | Nội dung thể hiện | Đưa vào mục báo cáo |
|---|---|---|---|
| `mobile_home.png` | 390 × 844 | Giao diện mobile-first 1 cột, co giãn vừa vặn màn hình điện thoại | Chương 6: Triển khai Mobile (Giao diện mobile) |
| `diabetes_mobile.png` | 390 × 844 | Thao tác nhập liệu và nhận chẩn đoán tiểu đường trên điện thoại di động | Chương 6: Triển khai Mobile (Demo Tiểu đường) |
| `house_mobile.png` | 390 × 844 | Thao tác định giá nhà bất động sản trên điện thoại di động | Chương 6: Triển khai Mobile (Demo Giá nhà) |
| `ecommerce_mobile.png` | 390 × 844 | Thao tác nhập nhận xét và phân tích hành vi khách hàng trên điện thoại | Chương 6: Triển khai Mobile (Demo E-Commerce) |

---

## 3. Swagger REST API Documentation (`screenshots/api/`)

| Tên Tệp | Khung nhìn | Nội dung thể hiện | Đưa vào mục báo cáo |
|---|---|---|---|
| `swagger_docs.png` | 1280 × 900 | Tài liệu tương tác OpenAPI / Swagger UI tại `/docs`, danh sách 4 endpoint | Chương 6: Triển khai REST API |
| `api_diabetes_result.png` | 1280 × 900 | Endpoint `POST /predict/diabetes` mở rộng với schema Pydantic | Chương 6: Chi tiết API Tiểu đường |
| `api_house_result.png` | 1280 × 900 | Endpoint `POST /predict/house` mở rộng với payload định giá | Chương 6: Chi tiết API Giá nhà |
| `api_ecommerce_result.png` | 1280 × 900 | Endpoint `POST /predict/ecommerce` mở rộng với payload đánh giá | Chương 6: Chi tiết API E-Commerce |
