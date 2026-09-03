# -*- coding: utf-8 -*-
"""
Chapter VI: Model Persistence and Deployment Architecture
"""

from .config import (
    add_styled_heading, add_body_p, add_bullet_p, add_code_block, add_code_snippet_with_notes, add_figure_with_notes
)

def build_chapter_6(doc):
    add_styled_heading(doc, "CHƯƠNG VI. PHƯƠNG PHÁP LƯU TRỮ VÀ TRIỂN KHAI MÔ HÌNH", 1)

    add_styled_heading(doc, "6.1. Tổng quan", 2)
    add_body_p(doc, "Sau khi hoàn thành nghiên cứu và lựa chọn được mô hình tối ưu trên tập kiểm thử, bước chuyển giao mang tính quyết định là đóng gói và đưa mô hình vào môi trường vận hành thực tế. Một mô hình không thể phát huy giá trị nếu chỉ nằm trong tệp .ipynb. Quy trình triển khai chuẩn khép kín trong dự án được thiết kế theo luồng:")
    add_code_block(doc,
"User Input ──> Pydantic Validation ──> Saved Preprocessing ──> Saved ML Model ──> Prediction ──> UI Display"
    )

    add_styled_heading(doc, "6.2. Lưu trữ mô hình (Model Persistence)", 2)
    add_body_p(doc, "Trong Python, thư viện joblib được lựa chọn làm giải pháp tuần tự hóa (serialization) chính thức thay cho pickle tiêu chuẩn. joblib được thiết kế đặc biệt tối ưu cho các cấu trúc mảng đa chiều NumPy và đường ống Scikit-Learn lớn, cho phép nén nhị phân nhanh và giảm thiểu chiếm dụng bộ nhớ RAM.")
    add_body_p(doc, "Thay vì lưu riêng lẻ trọng số mô hình rồi lưu riêng các giá trị trung bình chuẩn hóa (scaler), dự án đóng gói TOÀN BỘ ĐỐI TƯỢNG PIPELINE NGUYÊN KHỐI vào đúng một tệp duy nhất:")
    add_code_block(doc,
"import joblib\n\n"
"# Đóng gói toàn bộ chuỗi tiền xử lý và thuật toán suy luận\n"
"joblib.dump(full_pipeline, 'models/diabetes/diabetes_pipeline.joblib')\n"
"joblib.dump(full_pipeline, 'models/house_price/house_pipeline.joblib')\n"
"joblib.dump(full_pipeline, 'models/ecommerce/ecommerce_pipeline.joblib')"
    )

    add_styled_heading(doc, "6.3. Tính nhất quán giữa huấn luyện và dự đoán", 2)
    add_body_p(doc, "Yêu cầu nghiêm ngặt nhất của hệ thống triển khai là tính nhất quán toán học tuyệt đối (100% Mathematical Consistency) giữa môi trường huấn luyện và môi trường dự đoán. Khi người dùng nhập một hồ sơ mới từ giao diện Web, hệ thống tuyệt đối không được tạo mới bất kỳ scaler hay encoder nào. Toàn bộ các giá trị trung bình μ, độ lệch chuẩn σ, các quy tắc nhị phân của OneHotEncoder và từ điển 2,500 từ vựng TF-IDF đã học từ tập Train phải được tái sử dụng nguyên vẹn.")
    add_body_p(doc, "Thử nghiệm kiểm định độc lập đã được thực hiện bằng cách nạp lại các tệp .joblib từ đĩa cứng và kiểm tra suy luận trên 100 mẫu dữ liệu ngẫu nhiên. Kết quả chứng minh giá trị dự đoán khớp chính xác 100% (đến từng chữ số thập phân) so với kết quả tại thời điểm vừa huấn luyện trong Jupyter Notebook.")

    add_styled_heading(doc, "6.4. Triển khai mô hình dưới dạng Web Service với FastAPI", 2)
    add_body_p(doc, "Dịch vụ dự đoán REST API được xây dựng trong tệp api/main.py sử dụng framework FastAPI hiện đại. FastAPI mang lại các lợi thế kỹ thuật vượt trội: hiệu năng bất đồng bộ cao ngang ngửa NodeJS và Go, tự động xác thực dữ liệu đầu vào thông qua Pydantic Schemas, và tự động sinh tài liệu chuẩn Swagger UI tại đường dẫn /docs.")
    
    code_api_lifespan = '''@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load các pipelines học máy đã được huấn luyện (Persisted Models)
    diabetes_model = joblib.load(DIABETES_MODEL_PATH)
    house_model = joblib.load(HOUSE_MODEL_PATH)
    ecommerce_model = joblib.load(ECOMMERCE_MODEL_PATH)
    
    # Nạp vào bộ nhớ RAM toàn cục (Application State)
    app.state.models = {
        "diabetes": diabetes_model,
        "house": house_model,
        "ecommerce": ecommerce_model
    }
    yield
    app.state.models.clear()'''
    
    add_code_snippet_with_notes(
        doc,
        code_text=code_api_lifespan,
        caption_text="Đoạn mã 6.1. Khởi tạo và nạp mô hình vào bộ nhớ đệm (Lifespan Context Manager).",
        description_items=[
            "Toàn bộ 3 pipeline mô hình được nạp sẵn vào bộ nhớ RAM ngay tại thời điểm khởi động máy chủ (Startup).",
            "Giúp loại bỏ độ trễ đọc ổ cứng (Disk I/O Latency) cho từng request, bảo đảm thời gian phản hồi API luôn dưới 10 mili-giây."
        ],
        source_file="api/main.py"
    )

    code_api_predict = '''@app.post("/predict/diabetes")
async def predict_diabetes(data: DiabetesInput, request: Request):
    model = request.app.state.models.get("diabetes")
    
    # Chuyển đổi dữ liệu JSON từ Client thành pandas DataFrame 1 dòng
    input_df = pd.DataFrame([data.model_dump()])
    
    # Suy luận: Pipeline tự động tiền xử lý (Scale, Encode) và dự đoán
    prob = model.predict_proba(input_df)[0][1]
    pred = model.predict(input_df)[0]
    
    return {
        "prediction": int(pred),
        "probability": float(prob)
    }'''

    add_code_snippet_with_notes(
        doc,
        code_text=code_api_predict,
        caption_text="Đoạn mã 6.2. Endpoint dự đoán bệnh tiểu đường bằng REST API.",
        description_items=[
            "Endpoint tự động xác thực dữ liệu đầu vào thông qua schema `DiabetesInput` (Pydantic).",
            "Chuyển đổi dữ liệu JSON thành pandas DataFrame, truyền qua Pipeline (bao gồm tiền xử lý và suy luận) để trả về xác suất nguy cơ mắc bệnh."
        ],
        source_file="api/main.py"
    )


    add_figure_with_notes(
        doc,
        "screenshots/api/swagger_docs.png",
        "Hình 6.1. Giao diện Swagger UI của hệ thống REST API phục vụ toàn diện 3 bài toán thông minh.",
        [
            "Hệ thống định nghĩa đầy đủ các endpoint chuẩn RESTful: POST /predict/diabetes, POST /predict/house, POST /predict/ecommerce và GET /health.",
            "Mỗi endpoint đều được bảo vệ chặt chẽ bởi Pydantic Data Schemas, tự động xác thực kiểu dữ liệu, kiểm tra giới hạn giá trị và trả về mã lỗi 422 chi tiết nếu người dùng gửi tham số sai."
        ],
        explanation="Swagger UI tự động trích xuất schema từ FastAPI, cho phép kiểm thử trực tiếp các truy vấn HTTP ngay trên trình duyệt mà không cần cài đặt thêm phần mềm bên ngoài.",
        ml_implication="Kiến trúc API tách biệt hoàn toàn tầng tính toán học máy khỏi tầng giao diện người dùng, giúp hệ thống dễ dàng mở rộng và tích hợp vào bất kỳ ứng dụng nào."
    )

    add_styled_heading(doc, "6.5. Giao diện người dùng Web Application", 2)
    add_body_p(doc, "Giao diện Web được thiết kế theo phong cách Dark Mode Glassmorphism hiện đại tại web/templates/index.html và web/static/css/style.css, mang lại trải nghiệm tương tác cao cấp cho người dùng trên máy tính để bàn.")

    add_figure_with_notes(
        doc,
        "screenshots/web/web_home.png",
        "Hình 6.2. Giao diện trang chủ Web Application trên máy tính để bàn (Desktop Card UI).",
        [
            "Trang chủ tích hợp cả 3 ứng dụng thông minh trong một màn hình điều khiển thống nhất.",
            "Người dùng có thể chuyển đổi linh hoạt giữa các bài toán, nhập liệu vào các form được tối ưu hóa và nhận kết quả trực quan ngay lập tức kèm theo thanh đo độ tin cậy."
        ],
        explanation="Giao diện sử dụng HTML5, CSS thuần linh hoạt và JavaScript bất đồng bộ (Fetch API) để giao tiếp hai chiều với máy chủ FastAPI.",
        ml_implication="Trải nghiệm người dùng mượt mà giúp chuyển hóa các chỉ số xác suất khô khan của mô hình học máy thành thông điệp cảnh báo trực quan, dễ hiểu đối với bác sĩ, nhà đầu tư hoặc chuyên viên kinh doanh."
    )

    add_styled_heading(doc, "6.6. Triển khai trên ứng dụng Mobile", 2)
    add_body_p(doc, "Để người dùng có thể sử dụng điện thoại thông minh (Smartphone) thao tác trong thực tế, dự án đã triển khai giải pháp Responsive Mobile Web Client qua mạng Wi-Fi nội bộ LAN. Thiết kế đáp ứng chuẩn Mobile-First trên khung nhìn 390 × 844 px, bố cục chuyển đổi thông minh thành 1 cột dọc và không bị tràn lề ngang.")
    add_body_p(doc, "Điện thoại và máy tính chỉ cần kết nối cùng một mạng Wi-Fi. Người dùng mở trình duyệt Safari/Chrome trên smartphone và truy cập địa chỉ IP mạng nội bộ của máy chủ (ví dụ http://192.168.0.105:8000/). Do toàn bộ mã JavaScript sử dụng URL tương đối (/predict/...), các lệnh gọi API từ điện thoại tự động chuyển tới đúng máy chủ mà không gặp lỗi kết nối localhost.")

    add_figure_with_notes(
        doc,
        "screenshots/mobile/mobile_home.png",
        "Hình 6.3. Giao diện trang chủ hệ thống trên thiết bị di động truy cập qua mạng LAN (Viewport 390x844).",
        [
            "Bố cục giao diện co giãn hoàn hảo trên màn hình cảm ứng di động, các nút bấm và ô nhập liệu có kích thước đủ lớn, thuận tiện thao tác một tay.",
            "Người dùng trên điện thoại có thể thực hiện suy luận thời gian thực từ mô hình học máy đang chạy trên máy chủ."
        ],
        explanation="Thiết kế sử dụng kỹ thuật CSS Flexbox, CSS Grid và Media Queries (@media (max-width: 768px)) cùng các thẻ meta viewport chuẩn.",
        ml_implication="Giải pháp Responsive Web qua LAN mang lại tính cơ động cao như một ứng dụng di động thực thụ mà không đòi hỏi chi phí đóng gói, cấp chứng chỉ phức tạp như ứng dụng di động native.",
        max_width_inches=3.2
    )

    add_styled_heading(doc, "6.7. Kiến trúc hoàn chỉnh của hệ thống", 2)
    add_body_p(doc, "Mô hình kiến trúc tổng thể toàn chu trình từ người dùng tới mô hình tính toán:")
    add_code_block(doc,
"┌──────────────────────────────────────────────────────────────┐\n"
"│  NGƯỜI DÙNG CUỐI (CLIENT LAYER)                              │\n"
"│  • Desktop Web Browser (Chrome/Firefox/Edge)                 │\n"
"│  • Smartphone Mobile Browser (Safari/Chrome qua Wi-Fi LAN)   │\n"
"└──────────────────────────────┬───────────────────────────────┘\n"
"                               │ HTTP POST (JSON Payload)\n"
"                               ▼\n"
"┌──────────────────────────────────────────────────────────────┐\n"
"│  DỊCH VỤ DỰ ĐOÁN REST API (FASTAPI ENGINE)                   │\n"
"│  • Endpoint Routing (/predict/diabetes, /house, /ecommerce)  │\n"
"│  • Pydantic Schema Validation (Ràng buộc kiểu dữ liệu)       │\n"
"│  • Lifespan Model Cache (Nạp sẵn mô hình trong RAM)          │\n"
"└──────────────────────────────┬───────────────────────────────┘\n"
"                               │ pandas.DataFrame 1 dòng\n"
"                               ▼\n"
"┌──────────────────────────────────────────────────────────────┐\n"
"│  ĐƯỜNG ỐNG HỌC MÁY ĐÃ LƯU (SAVED SKLEARN PIPELINES)          │\n"
"│  • ColumnTransformer (StandardScaler, OneHot, TF-IDF)        │\n"
"│  • Estimator Inference (.predict(), .predict_proba())        │\n"
"└──────────────────────────────────────────────────────────────┘"
    )
