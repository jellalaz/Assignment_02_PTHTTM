# FINAL DELIVERABLE AUDIT & COMPLIANCE CHECKLIST
**Assignment 02 — Intelligent System Development (Posts and Telecommunications Institute of Technology)**

Tất cả các mục dưới đây phản ánh **chính xác 100% tình trạng thực tế** của dự án sau khi đã được thực thi và kiểm thử tự động.

---

## 1. Dữ Liệu Thực Nghiệm (Kaggle Datasets)
- [x] **Application 1 — Diabetes Dataset:** `ghnshymsaini/diabetes-prediction-dataset`
  - Đã tải về: `data/raw/diabetes/diabetes_prediction_dataset.csv` (100,000 dòng, 9 cột).
- [x] **Application 2 — House Price Dataset:** `chershi/house-price-prediction-dataset-2000-rows`
  - Đã tải về: `data/raw/house_price/enhanced_house_price_dataset.csv` (2,000 dòng, 16 cột).
- [x] **Application 3 — E-Commerce Dataset:** `nicapotato/womens-ecommerce-clothing-reviews`
  - Đã tải về: `data/raw/ecommerce/Womens Clothing E-Commerce Reviews.csv` (23,486 dòng, 11 cột).
- [x] **Dữ liệu giả lập (Synthetic Data):** **KHÔNG SỬ DỤNG**. 100% dữ liệu thật.

---

## 2. Notebooks & Huấn Luyện Học Máy (Jupyter Notebooks)
- [x] **01_diabetes.ipynb:**
  - Đầy đủ 25 mục cấu trúc chuẩn.
  - Đã chạy `Run All` thành công 100% bằng `jupyter nbconvert` với kernel `ai-env`.
  - 5 mô hình + Baseline (Logistic Regression, KNN, Decision Tree, Random Forest, SVM).
  - Đạt Recall = 89.70%, ROC-AUC = 0.9743 trên Test set.
- [x] **02_house_price.ipynb:**
  - Đầy đủ 25 mục cấu trúc chuẩn.
  - Đã chạy `Run All` thành công 100% bằng `jupyter nbconvert` với kernel `ai-env`.
  - 5 mô hình + Baseline (Linear, Ridge, Decision Tree, Random Forest, Gradient Boosting).
  - Đạt $R^2 = 0.7448$, MAE = $126,793.85 trên Test set.
- [x] **03_ecommerce.ipynb:**
  - Đầy đủ 25 mục cấu trúc chuẩn.
  - Phân biệt rõ ràng giữa TF-IDF Vector và Dense Embedding theory.
  - Đã chạy `Run All` thành công 100% bằng `jupyter nbconvert` với kernel `ai-env`.
  - So sánh 3 chế độ biểu diễn: Tabular Only vs Text TF-IDF vs Combined Tabular + Text.
  - Đạt ROC-AUC = 0.9737, Accuracy = 93.41% trên Test set.

---

## 3. Lưu Trữ Đường Ống (Model Persistence)
- [x] `models/diabetes/diabetes_pipeline.joblib`: Đóng gói `ColumnTransformer` + `RandomForestClassifier`.
- [x] `models/house_price/house_pipeline.joblib`: Đóng gói `ColumnTransformer` + `GradientBoostingRegressor`.
- [x] `models/ecommerce/ecommerce_pipeline.joblib`: Đóng gói `ColumnTransformer` (Tabular + TF-IDF) + `LogisticRegression`.
- [x] **Kiểm tra Reload & Suy luận:** Đã nạp lại bằng `joblib.load()` và thực hiện suy luận dự đoán thành công trên các mẫu mới.

---

## 4. Dịch Vụ Dự Đoán REST API (FastAPI)
- [x] API Server: `api/main.py` hỗ trợ Lifespan nạp sẵn model vào RAM.
- [x] Endpoint `POST /predict/diabetes`: Hoạt động chuẩn xác.
- [x] Endpoint `POST /predict/house`: Hoạt động chuẩn xác.
- [x] Endpoint `POST /predict/ecommerce`: Hoạt động chuẩn xác.
- [x] Endpoint `GET /health`: Báo cáo trạng thái cả 3 model sẵn sàng.
- [x] Swagger UI tại `/docs`: Tương tác trực quan đầy đủ.
- [x] Automated Tests `api/test_api.py`: 6/6 tests PASS qua `pytest`.

---

## 5. Triển Khai Giao Diện Web & Mobile
- [x] **Giao diện Desktop Web:** Thiết kế Dark Mode Glassmorphism hiện đại tại `web/templates/index.html` và `web/static/css/style.css`.
- [x] **Responsive Mobile Web Client qua LAN:** **DONE**
  - Hỗ trợ kết nối từ smartphone qua mạng Wi-Fi nội bộ (`http://192.168.0.105:8000/`).
  - Đường dẫn API tương đối (`/predict/...`) bảo đảm hoạt động thông suốt trên điện thoại.
  - Đã kiểm thử responsive trên khung nhìn điện thoại (`390 x 844`).
- [ ] **Native Flutter / Android Application:** **NOT IMPLEMENTED**
  - *Lý do:* Đã được thống nhất thay thế hoàn toàn bằng Responsive Mobile Web Client truy cập qua mạng LAN.

---

## 6. Minh Chứng Ảnh Chụp (Evidence Screenshots)
- [x] `screenshots/web/web_home.png`
- [x] `screenshots/web/diabetes_web_result.png`
- [x] `screenshots/web/house_web_result.png`
- [x] `screenshots/web/ecommerce_web_result.png`
- [x] `screenshots/mobile/mobile_home.png` (Viewport 390x844)
- [x] `screenshots/mobile/diabetes_mobile.png` (Viewport 390x844)
- [x] `screenshots/mobile/house_mobile.png` (Viewport 390x844)
- [x] `screenshots/mobile/ecommerce_mobile.png` (Viewport 390x844)
- [x] `screenshots/api/swagger_docs.png`
- [x] `screenshots/api/api_diabetes_result.png`
- [x] `screenshots/api/api_house_result.png`
- [x] `screenshots/api/api_ecommerce_result.png`

---

## 7. Tài Liệu Báo Cáo & Thảo Luận
- [x] `report/report_notes.md`: Báo cáo kỹ thuật chi tiết 9 chương theo chuẩn đề bài.
- [x] `report/discussion_questions.md`: Trả lời đầy đủ 15 câu hỏi chung + 6 câu hỏi E-Commerce bằng số liệu thực tế.
- [x] `DATASETS.md`: Hồ sơ dữ liệu chi tiết cho 3 bộ dữ liệu.
- [x] `README.md`: Hướng dẫn toàn diện tái lập dự án từ đầu.
- [x] `MOBILE_ACCESS_GUIDE.md`: Hướng dẫn chi tiết truy cập từ điện thoại qua mạng LAN.
- [x] `NEO4J_SETUP_GUIDE.md`: Hướng dẫn thiết lập và truy vấn Đồ thị Tri thức Neo4j.

---

## 8. Phần Mở Rộng Neo4j
- [x] Script Cypher `scripts/import_graph.cypher`: Tạo ràng buộc và truy vấn quan hệ.
- [x] Script Python `scripts/neo4j_demo.py`: Trích xuất mẫu dữ liệu và nạp vào Neo4j.
- [x] Hướng dẫn `NEO4J_SETUP_GUIDE.md`: Sẵn sàng cho người dùng cài đặt và chạy thử.
- [ ] **Neo4j Database Server đang chạy trên máy:** **OPTIONAL / CHƯA CHẠY** (Do Neo4j chưa được cài đặt sẵn trên máy host).

---

## ĐÁNH GIÁ MỨC ĐỘ SẴN SÀNG NỘP BÀI (READY FOR SUBMISSION)

**READY FOR SUBMISSION = YES**

### Giải thích:
- Toàn bộ 3 ứng dụng cốt lõi (Diabetes, House Price, E-Commerce) đã hoàn thành trọn vẹn từ Dữ liệu thô $\rightarrow$ Tiền xử lý $\rightarrow$ Biểu diễn số học $\rightarrow$ Huấn luyện mô hình $\rightarrow$ Đánh giá $\rightarrow$ Lưu trữ `.joblib` $\rightarrow$ REST API $\rightarrow$ Giao diện Web Desktop & Mobile LAN.
- Cả 3 Jupyter Notebooks đã được thực thi từ đầu tới cuối với kernel `ai-env` và lưu đầy đủ kết quả thực tế.
- Bộ test tự động `pytest` đạt 100% tỷ lệ pass (6/6 tests).
- Toàn bộ ảnh chụp minh chứng Web Desktop, Mobile Viewport và Swagger UI đã được hệ thống tự động tương tác và chụp thật.
- Báo cáo kỹ thuật và lời giải cho 21 câu hỏi thảo luận đã hoàn thiện với đầy đủ bảng biểu số liệu thực.
