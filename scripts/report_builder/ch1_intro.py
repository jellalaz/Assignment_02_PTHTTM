# -*- coding: utf-8 -*-
"""
Chapter I: Introduction and Problem Context
"""

from .config import (
    add_styled_heading, add_body_p, add_bullet_p, add_code_block, add_styled_table
)

def build_chapter_1(doc):
    add_styled_heading(doc, "CHƯƠNG I. TỔNG QUAN HỆ THỐNG VÀ BÀI TOÁN THỰC TẾ", 1)

    # Thêm Liên kết dự án
    add_styled_heading(doc, "LIÊN KẾT DỰ ÁN TRỰC TUYẾN", 2)
    add_bullet_p(doc, "https://assignment-02-pthttm.onrender.com/", bold_prefix="Web App Đã Triển Khai (Render): ")
    add_bullet_p(doc, "https://github.com/jellalaz/Assignment_02_PTHTTM", bold_prefix="Kho Mã Nguồn (GitHub): ")

    add_styled_heading(doc, "1.1. Lời mở đầu", 2)
    add_body_p(doc, "Trong thời đại cách mạng công nghiệp 4.0 và sự bùng nổ của trí tuệ nhân tạo (AI), việc khai phá tri thức tiềm ẩn từ các kho dữ liệu khổng lồ đã trở thành năng lực cốt lõi đối với mọi tổ chức và doanh nghiệp. Từ các bệnh viện cần công cụ hỗ trợ sàng lọc sớm bệnh lý hiểm nghèo, các công ty bất động sản cần hệ thống định giá nhà đất minh bạch, cho đến các sàn thương mại điện tử cần thấu hiểu tâm tư, nguyện vọng của khách hàng để tối ưu hóa trải nghiệm mua sắm — tất cả đều dựa trên nền tảng của các mô hình học máy (Machine Learning).")
    add_body_p(doc, "Tuy nhiên, trong thực tế phát triển phần mềm, một quan niệm sai lầm phổ biến là đồng nhất 'xây dựng hệ thống thông minh' với việc 'huấn luyện một thuật toán học máy'. Trên thực tế, thuật toán học máy chỉ là một mắt xích nhỏ nằm ở trung tâm của một chuỗi cung ứng kỹ thuật phức tạp. Một mô hình toán học dù có độ chính xác cao đến đâu trong môi trường nghiên cứu thực nghiệm cũng sẽ trở nên vô giá trị nếu không thể tiếp nhận dữ liệu thực tế, không thể triển khai trên hạ tầng mạng và không mang lại trải nghiệm tương tác trực quan cho người dùng cuối.")
    add_body_p(doc, "Nguyên lý cơ bản được nhấn mạnh trong học phần 'Phát triển các Hệ thống Thông minh' là: Dữ liệu thực tế không bao giờ tồn tại sẵn dưới dạng số học hoàn hảo. Dữ liệu thô từ thế giới thực luôn chứa đựng sự nhiễu loạn, khuyết thiếu, dị biệt về thang đo và cấu trúc đa phương thức (dạng bảng kết hợp văn bản tự do). Do đó, cây cầu nối quyết định tính sống còn của toàn bộ hệ thống chính là quá trình Biểu diễn Dữ liệu (Data Representation) kết hợp cùng đường ống tiền xử lý (Preprocessing Pipeline) chuẩn mực khoa học.")

    add_styled_heading(doc, "1.2. Mục tiêu của bài tập", 2)
    add_body_p(doc, "Bài tập lớn Assignment 02 được thiết kế với mục tiêu trang bị cho sinh viên tư duy hệ thống và kỹ năng kỹ thuật toàn diện, không chỉ dừng lại ở các dòng lệnh trong Jupyter Notebook mà hướng tới việc tạo ra sản phẩm phần mềm thông minh hoàn chỉnh có khả năng vận hành trong đời sống thực tế:")
    add_bullet_p(doc, "Nắm vững bản chất toán học của vector đặc trưng và ma trận đặc trưng, hiểu rõ cơ chế biến đổi các miền dữ liệu khác nhau (dữ liệu số, biến danh mục rời rạc, văn bản ngôn ngữ tự nhiên) thành không gian vector Euclid số chiều xác định.", bold_prefix="1. Nền tảng biểu diễn: ")
    add_bullet_p(doc, "Khai thác 100% dữ liệu thực tế từ nền tảng Kaggle trên ba miền bài toán hoàn toàn khác biệt. Nghiêm cấm hoàn toàn việc sử dụng dữ liệu nhân tạo hay số liệu giả lập, đối mặt trực tiếp với các thách thức thực tế như mất cân bằng nhãn và rò rỉ dữ liệu.", bold_prefix="2. Thực nghiệm trung thực: ")
    add_bullet_p(doc, "Xây dựng và so sánh khách quan hơn 16 thuật toán học máy có giám sát (từ Dummy Baseline, Linear/Logistic Regression, KNN, Decision Tree, Random Forest đến Gradient Boosting), lựa chọn độ đo đánh giá phù hợp với bản chất rủi ro của từng ngành nghề.", bold_prefix="3. Đánh giá đa chiều: ")
    add_bullet_p(doc, "Đóng gói toàn bộ quy trình tiền xử lý và mô hình suy luận thành các tệp nhị phân độc lập (.joblib), bảo đảm tính nhất quán toán học tuyệt đối giữa giai đoạn huấn luyện và giai đoạn vận hành.", bold_prefix="4. Đóng gói mô hình: ")
    add_bullet_p(doc, "Xây dựng máy chủ dịch vụ dự đoán REST API với framework FastAPI hiện đại (tự động sinh tài liệu chuẩn Swagger UI) và phát triển giao diện người dùng Responsive Web Application đa nền tảng, có khả năng phục vụ mượt mà trên cả máy tính Desktop lẫn điện thoại Smartphone qua mạng nội bộ Wi-Fi LAN.", bold_prefix="5. Triển khai ứng dụng: ")

    add_styled_heading(doc, "1.3. Quy trình phát triển hệ thống thông minh", 2)
    add_body_p(doc, "Tuân thủ nghiêm ngặt quy trình chuẩn kỹ nghệ dữ liệu khép kín, dự án được tổ chức thành một chuỗi 8 mắt xích liên tục:")
    add_code_block(doc,
"┌──────────┐     ┌───────────┐     ┌──────────┐     ┌──────────┐\n"
"│ Raw Data │ ──> │Understand │ ──> │  Clean   │ ──> │Represent │\n"
"└──────────┘     └───────────┘     └──────────┘     └──────────┘\n"
"                                                          │\n"
"┌──────────┐     ┌───────────┐     ┌──────────┐           │\n"
"│  Deploy  │ <── │  Persist  │ <── │ Evaluate │ <── ┌─────┴────┐\n"
"└──────────┘     └───────────┘     └──────────┘     │  Learn   │\n"
"                                                    └──────────┘"
    )
    add_bullet_p(doc, "Thu thập tệp dữ liệu thô từ Kaggle thông qua các script tự động hoặc API chuyên dụng, lưu trữ nguyên vẹn tại thư mục data/raw/.", bold_prefix="Bước 1 — Raw Data: ")
    add_bullet_p(doc, "Thực thi phân tích thống kê mô tả (df.shape, df.info(), df.describe()), xác định số lượng dòng/cột, phân loại kiểu dữ liệu (số học, chuỗi danh mục, văn bản) và kiểm tra phân bố biến mục tiêu.", bold_prefix="Bước 2 — Understand: ")
    add_bullet_p(doc, "Phát hiện và xử lý triệt để các vấn đề chất lượng dữ liệu: loại bỏ bản ghi trùng lặp (duplicate records), điền khuyết thiếu (imputation), rà soát giá trị không hợp lệ (invalid values) và thẩm tra giá trị cực biên (outliers).", bold_prefix="Bước 3 — Clean: ")
    add_bullet_p(doc, "Biến đổi dữ liệu sạch thành không gian vector số học d chiều: chuẩn hóa Z-score các biến số, mã hóa One-Hot với drop='first' cho biến danh mục và trích xuất đặc trưng TF-IDF cho văn bản bình luận.", bold_prefix="Bước 4 — Represent: ")
    add_bullet_p(doc, "Huấn luyện mô hình cơ sở tầm thường (Baseline) và 5+ thuật toán học máy cạnh tranh trên tập Train độc lập.", bold_prefix="Bước 5 — Learn: ")
    add_bullet_p(doc, "Đánh giá hiệu năng đa chỉ số trên tập Validation độc lập để chọn ra mô hình tối ưu nhất, sau đó kiểm định khách quan một lần duy nhất trên tập Test độc lập.", bold_prefix="Bước 6 — Evaluate: ")
    add_bullet_p(doc, "Đóng gói toàn bộ đối tượng ColumnTransformer và Estimator thành một Pipeline duy nhất thông qua joblib.dump(), lưu trữ tại thư mục models/.", bold_prefix="Bước 7 — Persist: ")
    add_bullet_p(doc, "Khởi chạy dịch vụ REST API với FastAPI, nạp sẵn Pipeline vào RAM và phục vụ người dùng thông qua giao diện Responsive Web Client truy cập qua mạng LAN.", bold_prefix="Bước 8 — Deploy: ")

    add_styled_heading(doc, "1.4. Tổng quan về ba ứng dụng", 2)
    add_body_p(doc, "Dự án triển khai thực tế trên ba bài toán thông minh độc lập, bao quát ba dạng cấu trúc dữ liệu và hai mô thức học máy chính:")

    add_styled_heading(doc, "1.4.1. Ứng dụng dự đoán bệnh tiểu đường (Diabetes Prediction)", 3)
    add_body_p(doc, "Tập trung vào lĩnh vực y tế dự phòng, bài toán đặt ra là phân loại nhị phân (Binary Classification) xem một bệnh nhân có thuộc nhóm nguy cơ mắc bệnh tiểu đường hay không dựa trên 8 chỉ số xét nghiệm và nhân khẩu học lâm sàng. Biến mục tiêu y nhận giá trị nhị phân {0: Không mắc bệnh, 1: Mắc bệnh tiểu đường}. Thách thức cốt lõi là tỷ lệ mất cân bằng nhãn nghiêm trọng (91.5% âm tính vs 8.5% dương tính) và đòi hỏi tối ưu hóa chỉ số Recall để tránh bỏ sót bệnh nhân.")

    add_styled_heading(doc, "1.4.2. Ứng dụng dự đoán giá nhà (House Price Prediction)", 3)
    add_body_p(doc, "Tập trung vào lĩnh vực kinh tế bất động sản, bài toán đặt ra là hồi quy giá trị liên tục (Continuous Regression) nhằm ước tính giá trị thị trường thực tế của một căn nhà dựa trên 15 đặc trưng vật lý và vị trí (diện tích sàn, số phòng ngủ, số phòng tắm, số tầng, tuổi thọ, thành phố và các tiện nghi đi kèm). Biến mục tiêu y là giá bán bằng USD. Thách thức lớn là việc kiểm soát hiện tượng đa cộng tuyến giữa các tiện nghi nhà và bảo đảm sai số tiền tệ MAE ở mức thấp nhất.")

    add_styled_heading(doc, "1.4.3. Ứng dụng phân tích hành vi và khám phá sở thích khách hàng thương mại điện tử", 3)
    add_body_p(doc, "Tập trung vào lĩnh vực thương mại điện tử (E-Commerce), bài toán đặt ra là phân loại đa phương thức (Multimodal Classification) kết hợp dữ liệu bảng định lượng (số sao đánh giá, tuổi, ngành hàng) với ngôn ngữ tự nhiên tự do (tiêu đề và nội dung nhận xét chi tiết) để dự đoán hành vi khuyến nghị sản phẩm (Recommended IND ∈ {0, 1}). Thách thức cốt lõi là chứng minh bằng thực nghiệm khoa học: Liệu việc bổ sung thông tin văn bản có thực sự cải thiện chất lượng mô hình so với chỉ sử dụng dữ liệu bảng truyền thống?")
