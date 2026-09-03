# -*- coding: utf-8 -*-
"""
Chapter X: Cross-System Comparison and Comprehensive Discussion Answers
"""

from docx.enum.text import WD_ALIGN_PARAGRAPH
from .config import (
    add_styled_heading, add_body_p, add_bullet_p, add_styled_table
)

def build_chapter_10(doc):
    add_styled_heading(doc, "CHƯƠNG X. SO SÁNH BA HỆ THỐNG THÔNG MINH", 1)

    add_styled_heading(doc, "10.1. So sánh bài toán và dữ liệu", 2)
    add_styled_table(
        doc,
        "Bảng 10.1. So sánh tổng hợp 11 tiêu chí kỹ thuật giữa ba hệ thống thông minh",
        ["Tiêu chí so sánh", "Ứng dụng 1: Diabetes", "Ứng dụng 2: House Price", "Ứng dụng 3: E-Commerce"],
        [
            ["Loại bài toán học máy", "Phân loại nhị phân (Classification)", "Hồi quy giá trị liên tục (Regression)", "Phân loại Đa phương thức (Tabular + NLP)"],
            ["Đối tượng quan sát (Unit)", "Một hồ sơ bệnh án lâm sàng", "Một căn nhà / bất động sản", "Một lượt đánh giá sản phẩm của khách hàng"],
            ["Biến mục tiêu (y)", "diabetes ∈ {0, 1}", "Price ∈ ℝ+ (USD)", "Recommended IND ∈ {0, 1}"],
            ["Dạng dữ liệu thô", "Bảng CSV (100,000 dòng, 9 cột)", "Bảng CSV (2,000 dòng, 16 cột)", "Bảng CSV + Văn bản (23,486 dòng, 11 cột)"],
            ["Kích thước sau làm sạch", "96,146 dòng (loại 3,854 trùng)", "2,000 dòng (0 thiếu, 0 trùng)", "23,486 dòng (nối văn bản hợp nhất)"],
            ["Số chiều đặc trưng (d)", "d = 13 chiều", "d = 23 chiều", "d = 2,532 chiều (32 bảng + 2,500 TF-IDF)"],
            ["Kích thước ma trận Train", "X_train ∈ ℝ^(67,302 × 13)", "X_train ∈ ℝ^(1,400 × 23)", "X_train ∈ ℝ^(16,440 × 2,532)"],
            ["Tiền xử lý then chốt", "Loại duplicate, Z-score, OneHot", "Z-score, OneHot (drop='first')", "Nối chuỗi, SimpleImputer, OneHot, TF-IDF"],
            ["Mô hình tối ưu nhất", "Random Forest Classifier", "Ridge Regression (α=1.0)", "Combined Tabular + TF-IDF LogReg"],
            ["Độ đo quyết định", "Recall = 0.8970, ROC-AUC = 0.9743", "MAE = $126,793, R² = 0.7448", "ROC-AUC = 0.9737, F1 = 0.9589"],
            ["Kiến trúc triển khai", "FastAPI + Responsive Web qua LAN", "FastAPI + Responsive Web qua LAN", "FastAPI + Responsive Web qua LAN"]
        ],
        col_widths=[1.8, 1.8, 1.8, 1.8],
        align_cols=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    )

    add_styled_heading(doc, "10.2. So sánh biểu diễn dữ liệu", 2)
    add_body_p(doc, "Sự khác biệt cốt lõi giữa ba ứng dụng nằm ở cấu trúc không gian hình học:")
    add_bullet_p(doc, "Không gian vector đặc (Dense Vector) số chiều thấp (d=13), các thuộc tính đều mang ý nghĩa sinh lý cụ thể.", bold_prefix="Tiểu đường: ")
    add_bullet_p(doc, "Không gian vector đặc liên tục (d=23), các biến số và biến chỉ thị nhị phân mô tả thuộc tính vật lý của công trình.", bold_prefix="Giá nhà: ")
    add_bullet_p(doc, "Không gian vector hỗn hợp đa phương thức số chiều lớn (d=2,532), kết hợp giữa 32 chiều bảng đặc (dense) với 2,500 chiều vector thưa (sparse) của ma trận TF-IDF.", bold_prefix="E-Commerce: ")

    add_styled_heading(doc, "10.3. So sánh quy trình tiền xử lý", 2)
    add_styled_heading(doc, "10.3.1. Các bước tiền xử lý chung", 3)
    add_body_p(doc, "Cả 3 ứng dụng đều tuân thủ nguyên tắc: Phân chia Train/Val/Test trước khi tiền xử lý, chuẩn hóa Z-score các biến số liên tục, mã hóa One-Hot các biến danh mục (kèm drop='first' và handle_unknown='ignore'), và đóng gói toàn bộ quy trình thành Scikit-Learn Pipeline nguyên khối.")

    add_styled_heading(doc, "10.3.2. Các bước tiền xử lý riêng biệt", 3)
    add_body_p(doc, "Tiểu đường đòi hỏi loại bỏ 3,854 bản ghi trùng lặp và phân tầng nhãn (stratify); Giá nhà đòi hỏi kiểm soát đa cộng tuyến của biến tiện nghi; E-Commerce đòi hỏi xử lý nối văn bản, lọc từ dừng tiếng Anh và tính toán ma trận TF-IDF 2,500 chiều.")

    add_styled_heading(doc, "10.4. So sánh mô hình học máy và độ đo", 2)
    add_body_p(doc, "Mỗi bài toán đòi hỏi một triết lý lựa chọn mô hình và độ đo đánh giá riêng biệt:")
    add_bullet_p(doc, "Mô hình cây tập hợp (Random Forest) chiến thắng nhờ khả năng học phi tuyến và hỗ trợ trọng số cân bằng lớp (balanced), ưu tiên tuyệt đối chỉ số Recall để bảo vệ tính mạng bệnh nhân.", bold_prefix="Tiểu đường: ")
    add_bullet_p(doc, "Mô hình hồi quy tuyến tính điều chuẩn (Ridge Regression) chiến thắng mô hình phi tuyến nhờ bản chất cộng dồn của giá trị nhà và khả năng triệt tiêu đa cộng tuyến của chuẩn L2, tối ưu hóa theo sai số tiền tệ MAE.", bold_prefix="Giá nhà: ")
    add_bullet_p(doc, "Mô hình tuyến tính đa biến (Logistic Regression) trên không gian kết hợp chiến thắng nhờ khả năng xử lý xuất sắc các vector thưa số chiều lớn (2,532 chiều) mà không bị bùng nổ tính toán, tối ưu theo chỉ số phân tách ROC-AUC.", bold_prefix="E-Commerce: ")

    add_styled_heading(doc, "10.5. So sánh kiến trúc triển khai", 2)
    add_body_p(doc, "Cả 3 ứng dụng đều được quy chuẩn hóa thống nhất vào cùng một hệ thống máy chủ REST API (FastAPI) và một giao diện Responsive Web Client duy nhất. Kiến trúc hướng dịch vụ microservices này giúp việc mở rộng thêm các mô hình mới trong tương lai diễn ra độc lập mà không ảnh hưởng đến giao diện người dùng.")

    add_styled_heading(doc, "10.6. Trả lời các câu hỏi thảo luận", 2)

    # 10.6.1 DIABETES 15 QUESTIONS
    add_styled_heading(doc, "10.6.1. Trả lời 15 câu hỏi thảo luận cho Ứng dụng 1 (Dự đoán bệnh tiểu đường)", 3)
    
    add_body_p(doc, "Một quan sát đại diện cho một hồ sơ bệnh án lâm sàng của một bệnh nhân cụ thể, chứa các thông số nhân khẩu học (tuổi, giới tính) và kết quả xét nghiệm sinh hóa tại thời điểm kiểm tra y tế.", bold_prefix="Câu 1 (Observation): ")
    add_body_p(doc, "Tệp dữ liệu bảng CSV gồm 100,000 dòng và 9 cột thuộc tính.", bold_prefix="Câu 2 (Raw Representation): ")
    add_body_p(doc, "Một vector đặc trưng số học chuẩn hóa x_i ∈ ℝ^13, ma trận huấn luyện X_train ∈ ℝ^(67,302 × 13).", bold_prefix="Câu 3 (Final Numerical Representation): ")
    add_body_p(doc, "Chiều N = 67,302 là số lượng bệnh nhân trong tập Train; chiều d = 13 là số đặc trưng sau chuẩn hóa và mã hóa.", bold_prefix="Câu 4 (Shape dimensions): ")
    add_body_p(doc, "Hai biến danh mục: gender (Female, Male, Other) và smoking_history (never, current, former, ...).", bold_prefix="Câu 5 (Encoding): ")
    add_body_p(doc, "Sáu biến số học: age, bmi, HbA1c_level, blood_glucose_level, hypertension, heart_disease.", bold_prefix="Câu 6 (Scaling): ")
    add_body_p(doc, "Z-score làm mất đơn vị đo vật lý (năm tuổi, kg/m², mg/dL). Việc lọc 3,854 bản ghi trùng làm giảm nhẹ tần suất tự nhiên của mẫu điển hình.", bold_prefix="Câu 7 (Information lost): ")
    add_body_p(doc, "Phân bố tương đối, tương quan giữa các biến lâm sàng và khả năng phân tách nhãn bệnh.", bold_prefix="Câu 8 (Information preserved): ")
    add_body_p(doc, "Gọi fit() trên toàn bộ dữ liệu trước khi chia tập. Khắc phục: Chia tập trước, chỉ fit trên Train.", bold_prefix="Câu 9 (Data Leakage): ")
    add_body_p(doc, "Random Forest Classifier với class_weight='balanced'.", bold_prefix="Câu 10 (Best Model): ")
    add_body_p(doc, "Bắt được mối quan hệ phi tuyến phức tạp giữa đường huyết và các yếu tố cơ địa; cơ chế balanced giúp bao phủ toàn bộ lớp thiểu số mắc bệnh.", bold_prefix="Câu 11 (Why Chosen): ")
    add_body_p(doc, "Recall (0.8970) và ROC-AUC (0.9743) nhằm triệt tiêu tối đa ca âm tính giả (False Negative).", bold_prefix="Câu 12 (Crucial Metric): ")
    add_body_p(doc, "Đóng gói ColumnTransformer và Random Forest thành Pipeline duy nhất qua joblib.dump().", bold_prefix="Câu 13 (Model Persistence): ")
    add_body_p(doc, "FastAPI nạp tệp .joblib vào RAM khi khởi động, tiếp nhận JSON, chuyển thành DataFrame và gọi pipeline.predict().", bold_prefix="Câu 14 (Web Service Usage): ")
    add_body_p(doc, "Trình duyệt Safari/Chrome trên smartphone kết nối qua Wi-Fi LAN gọi API bằng Fetch API qua URL tương đối.", bold_prefix="Câu 15 (Mobile Client Communication): ")

    # 10.6.2 HOUSE PRICE 15 QUESTIONS
    add_styled_heading(doc, "10.6.2. Trả lời 15 câu hỏi thảo luận cho Ứng dụng 2 (Dự đoán giá nhà)", 3)
    
    add_body_p(doc, "Một quan sát đại diện cho một căn nhà / bất động sản nhà ở cụ thể đã hoàn thành giao dịch trên thị trường.", bold_prefix="Câu 1 (Observation): ")
    add_body_p(doc, "Tệp bảng CSV gồm 2,000 dòng và 16 cột thông số kiến trúc và tiện nghi.", bold_prefix="Câu 2 (Raw Representation): ")
    add_body_p(doc, "Một vector liên tục x_i ∈ ℝ^23, ma trận huấn luyện X_train ∈ ℝ^(1,400 × 23).", bold_prefix="Câu 3 (Final Numerical Representation): ")
    add_body_p(doc, "Chiều N = 1,400 là số lượng căn nhà huấn luyện; chiều d = 23 là số đặc trưng sau mã hóa.", bold_prefix="Câu 4 (Shape dimensions): ")
    add_body_p(doc, "Tám biến danh mục: City, Furnishing, Main Road, Guest Room, Basement, Water Supply, Air Conditioning, Preferred Tenant.", bold_prefix="Câu 5 (Encoding): ")
    add_body_p(doc, "Bảy biến số học: Area, Bedrooms, Bathrooms, Stories, Parking, Age, Locality Rating.", bold_prefix="Câu 6 (Scaling): ")
    add_body_p(doc, "Z-score làm mất đơn vị đo sq ft, số phòng gốc. drop='first' loại bỏ một giá trị danh mục làm mốc tham chiếu.", bold_prefix="Câu 7 (Information lost): ")
    add_body_p(doc, "Tương quan tuyến tính mạnh giữa diện tích, tiện nghi với giá nhà được bảo toàn trọn vẹn.", bold_prefix="Câu 8 (Information preserved): ")
    add_body_p(doc, "Chuẩn hóa biến mục tiêu hoặc biến đầu vào trên toàn bộ 2,000 dòng trước khi tách tập 70/15/15.", bold_prefix="Câu 9 (Data Leakage): ")
    add_body_p(doc, "Ridge Regression (kết hợp Gradient Boosting kiểm chứng).", bold_prefix="Câu 10 (Best Model): ")
    add_body_p(doc, "Giá nhà có bản chất cộng dồn tuyến tính; điều chuẩn L2 của Ridge triệt tiêu hiện tượng đa cộng tuyến hoàn hảo giữa các tiện nghi nhà.", bold_prefix="Câu 11 (Why Chosen): ")
    add_body_p(doc, "MAE ($126,793) và R² (0.7448) vì đo lường trực tiếp sai lệch tiền tệ thực tế.", bold_prefix="Câu 12 (Crucial Metric): ")
    add_body_p(doc, "Lưu toàn bộ Pipeline tiền xử lý và Ridge Regression vào tệp models/house_price/house_pipeline.joblib.", bold_prefix="Câu 13 (Model Persistence): ")
    add_body_p(doc, "FastAPI nạp sẵn mô hình trong RAM, nhận JSON gửi lên, suy luận tích vô hướng w^T x + b và trả về số tiền định giá.", bold_prefix="Câu 14 (Web Service Usage): ")
    add_body_p(doc, "Giao diện Responsive Web thích ứng hoàn hảo trên màn hình cảm ứng di động, gửi request qua mạng LAN.", bold_prefix="Câu 15 (Mobile Client Communication): ")

    # 10.6.3 ECOMMERCE 15 QUESTIONS
    add_styled_heading(doc, "10.6.3. Trả lời 15 câu hỏi thảo luận cho Ứng dụng 3 (E-Commerce Customer Behavior)", 3)
    
    add_body_p(doc, "Một quan sát đại diện cho một lượt đánh giá sản phẩm may mặc của một khách hàng nữ trên sàn thương mại điện tử.", bold_prefix="Câu 1 (Observation): ")
    add_body_p(doc, "Tệp CSV gồm 23,486 dòng chứa cả thông tin bảng số và hai trường văn bản tự do Title và Review Text.", bold_prefix="Câu 2 (Raw Representation): ")
    add_body_p(doc, "Một vector hỗn hợp đa phương thức x_i ∈ ℝ^2,532 (32 chiều bảng + 2,500 chiều TF-IDF).", bold_prefix="Câu 3 (Final Numerical Representation): ")
    add_body_p(doc, "Chiều N = 16,440 là số lượt đánh giá trong tập Train; d = 2,532 là tổng số chiều bảng và từ vựng n-gram.", bold_prefix="Câu 4 (Shape dimensions): ")
    add_body_p(doc, "Ba biến danh mục sản phẩm: Division Name, Department Name, Class Name.", bold_prefix="Câu 5 (Encoding): ")
    add_body_p(doc, "Ba biến số: Age, Rating, Positive Feedback Count.", bold_prefix="Câu 6 (Scaling): ")
    add_body_p(doc, "TF-IDF làm mất trật tự cú pháp từ ngữ trong câu, sắc thái ngữ điệu và mối liên hệ giữa các từ đồng nghĩa.", bold_prefix="Câu 7 (Information lost): ")
    add_body_p(doc, "Tần suất các từ khóa cảm xúc then chốt (love, perfect, cheap, returned, runs small) được bảo toàn nguyên vẹn.", bold_prefix="Câu 8 (Information preserved): ")
    add_body_p(doc, "Khởi tạo TfidfVectorizer.fit() trên toàn bộ 23,486 bình luận trước khi phân chia tập.", bold_prefix="Câu 9 (Data Leakage): ")
    add_body_p(doc, "Combined Tabular + TF-IDF Logistic Regression.", bold_prefix="Câu 10 (Best Model): ")
    add_body_p(doc, "Logistic Regression xử lý cực kỳ xuất sắc và ổn định trên không gian ma trận thưa số chiều lớn (2,532 chiều) mà không bị bùng nổ tính toán.", bold_prefix="Câu 11 (Why Chosen): ")
    add_body_p(doc, "ROC-AUC (0.9737) và F1-Score (0.9589) phản ánh chính xác năng lực phân định trên dữ liệu nhãn lệch (82/18).", bold_prefix="Câu 12 (Crucial Metric): ")
    add_body_p(doc, "Đóng gói đối tượng FeatureUnion/ColumnTransformer và Logistic Regression vào ecommerce_pipeline.joblib.", bold_prefix="Câu 13 (Model Persistence): ")
    add_body_p(doc, "API nạp pipeline, tự động ghép chuỗi Title + Review, vector hóa TF-IDF và đưa ra xác suất khuyến nghị.", bold_prefix="Câu 14 (Web Service Usage): ")
    add_body_p(doc, "Khách hàng nhập trực tiếp văn bản từ bàn phím điện thoại, giao diện di động gửi HTTP POST qua LAN và nhận kết quả tức thì.", bold_prefix="Câu 15 (Mobile Client Communication): ")

    # 10.6.4 ECOMMERCE 6 SUPPLEMENTARY QUESTIONS
    add_styled_heading(doc, "10.6.4. Trả lời 6 câu hỏi thảo luận bổ sung chuyên sâu cho E-Commerce", 3)
    
    add_body_p(doc, "Nội dung nhận xét phản ánh những trải nghiệm chủ quan sâu sắc: Độ vừa vặn của trang phục (runs small, true to size), chất lượng chất liệu vải (soft, itchy, cheap fabric), tính thẩm mỹ màu sắc và ý định hành vi (dự định mặc đi tiệc hoặc đem trả hàng).", bold_prefix="1. Nội dung văn bản nhận xét chứa đựng những thông tin gì? ")
    add_body_p(doc, "Nối tiêu đề và nội dung → Tách từ (Tokenization unigram + bigram) → Loại bỏ stop words tiếng Anh → Tính trọng số thống kê TF-IDF → Chuẩn hóa vector chuẩn L2 trong không gian ℝ^2500.", bold_prefix="2. Văn bản nhận xét được chuyển đổi thành dữ liệu số như thế nào? ")
    add_body_p(doc, "Theo bài giảng Lecture 02, Token ID là một số nguyên duy nhất đại diện cho chỉ số của một từ hoặc mảnh từ trong từ điển từ vựng cố định. Ví dụ ['I', 'love', 'this'] → [42, 1892, 48]. Token ID đóng vai trò con trỏ chỉ mục để tra cứu vector trong bảng nhúng.", bold_prefix="3. Token IDs trong bài giảng Lecture 02 đại diện cho điều gì? ")
    add_body_p(doc, "Embedding Vector là một vector đặc (dense) số chiều thấp (64 – 768 chiều) biểu diễn tọa độ ngữ nghĩa của từ trong không gian liên tục, nơi các từ đồng nghĩa có khoảng cách Cosine gần nhau. Ngược lại, TF-IDF là vector thưa (sparse) số chiều lớn và không thể hiện tính đồng nghĩa.", bold_prefix="4. Vector nhúng (Embedding Vectors) đại diện cho điều gì? ")
    add_body_p(doc, "Phát hiện mối liên hệ ranh giới tại nhóm 3 sao; phát hiện hai ngành hàng quan tâm chủ lực là Áo (Tops) và Váy đầm (Dresses); nhận diện các từ khóa biểu đạt sự hài lòng cao nhất (love, flattering, comfortable).", bold_prefix="5. Những sở thích hoặc hành vi khách hàng nào có thể khám phá được? ")
    add_body_p(doc, "CÓ. Thực nghiệm chứng minh ROC-AUC tăng từ 0.9819 (Tabular) lên 0.9877 (Combined) trên Validation và 0.9737 trên Test. Văn bản nhận xét giải quyết triệt để các ca phân vân tại mức 3 sao mà điểm số đơn thuần không phân tách được.", bold_prefix="6. Nội dung văn bản có thực sự cải thiện chất lượng mô hình? ")
