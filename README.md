# Phát triển Hệ thống Thông minh 🚀

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4.1-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.12-008CC1?logo=neo4j&logoColor=white)](https://neo4j.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://docker.com)

**Học viện Công nghệ Bưu chính Viễn thông (PTIT)**  
**Môn học:** Phát triển các hệ thống thông minh (Intelligent System Development)  
**Giảng viên hướng dẫn:** PGS. TS. Trần Đình Quế  

---

## 🎯 1. Tổng quan & Ứng dụng

Dự án này triển khai một quy trình hệ thống thông minh toàn diện từ đầu đến cuối, xóa nhòa khoảng cách giữa các tập dữ liệu thô và một dịch vụ web thực tế sẵn sàng triển khai:

$$\text{Dữ liệu thô} \longrightarrow \text{Làm sạch} \longrightarrow \text{Biểu diễn} \longrightarrow \text{Huấn luyện} \longrightarrow \text{Đánh giá} \longrightarrow \text{Triển khai}$$

Hệ thống tích hợp **ba ứng dụng học máy đa dạng**, sử dụng các kỹ thuật xử lý dữ liệu dạng bảng (Tabular) và xử lý ngôn ngữ tự nhiên (NLP) trên **100% dữ liệu Kaggle thực tế**:

### 🩺 A. Dự đoán Bệnh Tiểu Đường (Phân loại Y tế)
- **Tập dữ liệu:** 100,000 hồ sơ bệnh án (Dữ liệu mất cân bằng).
- **Kỹ thuật:** Chuẩn hóa Standard Scaling, Mã hóa One-Hot, Xử lý mất cân bằng (SMOTE / Balanced Weights).
- **Mô hình tốt nhất:** **Random Forest Classifier** (Recall = 89.70%, ROC-AUC = 0.9743).
- **Giá trị thực tiễn:** Ngăn ngừa việc bỏ lọt bệnh nhân (false negatives) trong tầm soát bệnh tiểu đường.

### 🏠 B. Dự đoán Giá Nhà (Hồi quy Bất động sản)
- **Tập dữ liệu:** 2,000 hồ sơ bất động sản đa dạng.
- **Kỹ thuật:** Xóa bỏ giá trị ngoại lai (Outliers), Phân tích tương quan đặc trưng (Correlation).
- **Mô hình tốt nhất:** **Gradient Boosting Regressor** ($R^2 = 0.7448$, MAE = $126,793).
- **Giá trị thực tiễn:** Định giá bất động sản với độ chính xác cao dựa trên các chỉ số cấu trúc và vị trí địa lý.

### 🛍️ C. Hành vi Khách hàng Thương mại Điện tử (Phân loại Đa phương thức)
- **Tập dữ liệu:** 23,486 đánh giá quần áo nữ (Bao gồm dữ liệu dạng Bảng + Văn bản).
- **Kỹ thuật:** **TF-IDF Vectorization** (Văn bản) + Chuẩn hóa Standard (Bảng) kết hợp qua `ColumnTransformer`.
- **Mô hình tốt nhất:** **Logistic Regression** trên Đặc trưng kết hợp (Độ chính xác = 93.41%, ROC-AUC = 0.9737).
- **Giá trị thực tiễn:** Tự động phân loại cảm xúc khách hàng và trạng thái khuyên dùng sản phẩm dựa trên văn bản đánh giá thô.

---

## 🌐 2. Phần Mở Rộng: Đồ thị Tri thức Neo4j (Graph RAG)

Các mô hình Học máy truyền thống coi dữ liệu như những hàng đơn lẻ độc lập. Để vượt qua giới hạn này trong module Thương mại điện tử, hệ thống được thiết kế thêm **Kiến trúc Đồ thị Tri thức (Knowledge Graph)** bằng cơ sở dữ liệu **Neo4j**.

Bằng cách chuyển đổi dữ liệu dạng bảng thành một mạng lưới liên kết (`Khách hàng` $\rightarrow$ `VIẾT` $\rightarrow$ `Đánh giá` $\rightarrow$ `VỀ` $\rightarrow$ `Sản phẩm`), hệ thống tạo tiền đề cho **Graph RAG (Retrieval-Augmented Generation)**, cho phép Chatbot trả lời các câu hỏi phức tạp như: *"Những khách hàng nữ dưới 30 tuổi đánh giá thế nào về mẫu váy mùa hè của chúng ta?"*

- **Hướng dẫn cài đặt:** Xem file [NEO4J_SETUP_GUIDE.md](NEO4J_SETUP_GUIDE.md).
- **Cấu trúc Cypher (Constraints):** Nằm tại `scripts/import_graph.cypher`.
- **Demo kết nối Python:** Chạy lệnh `python scripts/neo4j_demo.py` để tự động xây dựng đồ thị từ file CSV và chạy thử giả lập Graph RAG trên máy của bạn.

---

## 🏗️ 3. Kiến trúc Hệ thống & Triển khai

Hệ thống được triển khai dưới dạng kiến trúc hiện đại, phân tách độc lập (decoupled):

1. **Inference Engine (FastAPI):** Cung cấp các API `/predict/diabetes`, `/predict/house`, và `/predict/ecommerce`. Các mô hình học máy được tải sẵn vào RAM bằng `lifespan` context manager, đảm bảo độ trễ phản hồi cực thấp (dưới 10ms).
2. **Kiểm tra dữ liệu (Validation):** Pydantic `v2` đảm bảo kiểm tra chặt chẽ kiểu dữ liệu cho toàn bộ payload JSON đầu vào.
3. **Frontend Dashboard:** Giao diện Web thiết kế theo phong cách Glassmorphism (HTML/CSS/JS) tương tác bất đồng bộ với backend FastAPI qua `Fetch API`.
4. **Tương thích Mobile LAN:** Giao diện web được thiết kế responsive cực tốt, cho phép truy cập dễ dàng bằng điện thoại di động qua mạng Wi-Fi cục bộ (LAN).

---

## 🚀 4. Hướng dẫn Khởi chạy Nhanh (Quickstart)

### Bước 1: Thiết lập môi trường
Dự án này yêu cầu chạy bằng môi trường Conda **`ai-env`** (Python 3.12).
```bash
conda activate ai-env
pip install -r requirements.txt
```

### Bước 2: Tải & Tiền xử lý dữ liệu
```bash
# Tải tự động các tập dữ liệu thô từ Kaggle vào thư mục data/raw/
python scripts/download_datasets.py

# Chạy các pipeline làm sạch dữ liệu và huấn luyện mô hình (xuất file .joblib vào models/)
python src/diabetes/pipeline.py
python src/house_price/pipeline.py
python src/ecommerce/pipeline.py
```

### Bước 3: Chạy Server (API & Web)
Khởi chạy ứng dụng FastAPI trên `0.0.0.0` để có thể truy cập qua cả Localhost và mạng LAN:
```bash
PYTHONPATH=. uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
- **Web Dashboard:** [http://localhost:8000/](http://localhost:8000/)
- **Tài liệu API (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)

### Bước 4: Triển khai bằng Docker (Tùy chọn)
Dự án đã được tối ưu hóa với `Dockerfile` và `render.yaml` phục vụ cho việc triển khai lên Cloud.
```bash
docker build -t intelligent-system .
docker run -p 8000:8000 -e PORT=8000 intelligent-system
```

---

## 📸 5. Báo cáo & Tài liệu trực quan
Toàn bộ ảnh chụp màn hình chứng minh sản phẩm (Giao diện Desktop, Giao diện Mobile, Swagger API) được tạo tự động bằng Selenium Headless Chrome. Vui lòng xem thư mục `screenshots/`.

Một **Báo cáo kỹ thuật chi tiết dài 84 trang** (`report/Baocao.pdf`) đã được biên dịch tự động hoàn chỉnh, kết hợp mượt mà giữa phương pháp lý thuyết, mã nguồn thực tế, và biểu đồ EDA trực quan sinh động.
