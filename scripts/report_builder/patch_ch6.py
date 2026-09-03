import re

with open("scripts/report_builder/ch6_deployment_methods.py", "r", encoding="utf-8") as f:
    content = f.read()

# Make sure we import add_code_snippet_with_notes
if "add_code_snippet_with_notes" not in content:
    content = content.replace(
        "add_styled_heading, add_body_p, add_bullet_p, add_code_block,",
        "add_styled_heading, add_body_p, add_bullet_p, add_code_block, add_code_snippet_with_notes,"
    )

# Snippet 1 & 2 insertion
snippet = """    add_styled_heading(doc, "6.4. Triển khai mô hình dưới dạng Web Service với FastAPI", 2)
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
"""
content = content.replace('    add_styled_heading(doc, "6.4. Triển khai mô hình dưới dạng Web Service với FastAPI", 2)\n    add_body_p(doc, "Dịch vụ dự đoán REST API được xây dựng trong tệp api/main.py sử dụng framework FastAPI hiện đại. FastAPI mang lại các lợi thế kỹ thuật vượt trội: hiệu năng bất đồng bộ cao ngang ngửa NodeJS và Go, tự động xác thực dữ liệu đầu vào thông qua Pydantic Schemas, và tự động sinh tài liệu chuẩn Swagger UI tại đường dẫn /docs.")', snippet)

# Remove the old text that snippet replaces
content = content.replace('    add_body_p(doc, "Toàn bộ 3 pipeline mô hình được nạp sẵn vào bộ nhớ RAM ngay tại thời điểm khởi động máy chủ thông qua Lifespan Context Manager, giúp loại bỏ độ trễ nạp đĩa (Disk I/O Latency) và bảo đảm thời gian phản hồi mỗi request dưới 10 mili-giây.")\n', '')

with open("scripts/report_builder/ch6_deployment_methods.py", "w", encoding="utf-8") as f:
    f.write(content)
