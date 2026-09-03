# -*- coding: utf-8 -*-
"""
Chapter III: Data Preprocessing Methodology
"""

from .config import (
    add_styled_heading, add_body_p, add_bullet_p, add_code_block, add_styled_table
)

def build_chapter_3(doc):
    add_styled_heading(doc, "CHƯƠNG III. PHƯƠNG PHÁP TIỀN XỬ LÝ DỮ LIỆU", 1)

    add_styled_heading(doc, "3.1. Tìm hiểu dữ liệu (Data Understanding)", 2)
    add_body_p(doc, "Giai đoạn Tìm hiểu Dữ liệu đóng vai trò thiết lập nền móng cho toàn bộ chu trình xử lý. Thay vì vội vã đưa dữ liệu vào huấn luyện, kỹ sư học máy bắt buộc phải trả lời được các câu hỏi cơ bản: Quy mô quan sát là bao nhiêu? Có bao nhiêu thuộc tính đầu vào? Kiểu dữ liệu của từng cột là gì? Có thuộc tính nào bị thiếu hay chứa giá trị dị thường không?")
    add_body_p(doc, "Các câu lệnh cơ bản trong thư viện Pandas được áp dụng để trích xuất bức tranh tổng thể về dữ liệu:")
    add_code_block(doc,
"# 1. Kiểm tra kích thước số dòng, số cột\n"
">>> df.shape\n\n"
"# 2. Kiểm tra kiểu dữ liệu và số lượng giá trị non-null trên từng cột\n"
">>> df.info()\n\n"
"# 3. Thống kê mô tả các biến số (mean, std, min, 25%, 50%, 75%, max)\n"
">>> df.describe()\n\n"
"# 4. Thống kê mô tả các biến phân loại chuỗi (count, unique, top, freq)\n"
">>> df.describe(include=['object'])"
    )

    add_styled_heading(doc, "3.2. Làm sạch dữ liệu", 2)
    add_body_p(doc, "Chất lượng của dữ liệu đầu vào quyết định trực tiếp trần hiệu năng của mô hình ('Garbage in, Garbage out'). Quá trình làm sạch dữ liệu trong dự án tập trung giải quyết 4 vấn đề kỹ thuật:")

    add_styled_heading(doc, "3.2.1. Xử lý giá trị thiếu (Missing Values)", 3)
    add_body_p(doc, "Giá trị khuyết thiếu xuất hiện do lỗi thu thập, thiết bị cảm biến hỏng hóc hoặc người dùng từ chối cung cấp thông tin. Trong thống kê học, giá trị thiếu được phân loại thành:")
    add_bullet_p(doc, "Giá trị thiếu hoàn toàn ngẫu nhiên (Missing Completely at Random - MCAR).", bold_prefix="MCAR: ")
    add_bullet_p(doc, "Giá trị thiếu ngẫu nhiên phụ thuộc vào các biến quan sát khác (Missing at Random - MAR).", bold_prefix="MAR: ")
    add_bullet_p(doc, "Giá trị thiếu không ngẫu nhiên, phụ thuộc vào chính giá trị bị thiếu (Missing Not at Random - MNAR).", bold_prefix="MNAR: ")
    add_body_p(doc, "Chiến lược xử lý tùy thuộc vào tỷ lệ và tính chất của thuộc tính: Nếu tỷ lệ thiếu dưới 5% và là biến số, có thể điền bằng giá trị trung bình (Mean) nếu phân bố chuẩn, hoặc trung vị (Median) nếu phân bố lệch; nếu là biến danh mục, điền bằng giá trị phổ biến nhất (Mode) hoặc gán nhãn riêng 'Unknown'. Nếu là văn bản tự do, điền chuỗi rỗng '' để ghép chuỗi.")
    add_styled_table(
        doc,
        "Bảng 3.1. Tổng hợp tình trạng giá trị thiếu và phương pháp xử lý trên ba tập dữ liệu thực tế",
        ["Tập dữ liệu", "Quy mô", "Số cột có Missing", "Thuộc tính bị thiếu", "Phương pháp xử lý áp dụng"],
        [
            ["Diabetes Prediction", "100,000 dòng", "0 cột (0 missing)", "Không có", "Dữ liệu hoàn hảo, không cần điền"],
            ["House Price Prediction", "2,000 dòng", "0 cột (0 missing)", "Không có", "Dữ liệu hoàn hảo, không cần điền"],
            ["E-Commerce Reviews", "23,486 dòng", "5 cột", "Title (3,810), Review Text (845), Division/Dept/Class (14)", "Title/Review: Điền chuỗi rỗng ''; Danh mục: SimpleImputer 'Unknown'"]
        ],
        col_widths=[1.5, 1.0, 1.2, 1.8, 1.7]
    )

    add_styled_heading(doc, "3.2.2. Xử lý dữ liệu trùng lặp (Duplicate Records)", 3)
    add_body_p(doc, "Bản ghi trùng lặp là các dòng giống nhau hoàn toàn trên mọi thuộc tính. Sự xuất hiện của các bản ghi trùng lặp làm sai lệch tần suất xuất hiện tự nhiên của các mẫu, làm suy giảm tính đa dạng dữ liệu, và nguy hiểm nhất là gây ra hiện tượng rò rỉ dữ liệu khi một bản ghi trùng lặp rơi vào tập Train còn bản sao của nó rơi vào tập Test.")
    add_code_block(doc,
"# Kiểm tra số lượng bản ghi trùng lặp hoàn toàn\n"
">>> df.duplicated().sum()\n"
"3854   # Phát hiện chính xác 3,854 bản ghi trùng trong tập Diabetes thô\n\n"
"# Loại bỏ và kiểm tra lại kích thước mới\n"
">>> df_clean = df.drop_duplicates()\n"
">>> df_clean.shape\n"
"(96146, 9)   # Kích thước sạch độc lập"
    )

    add_styled_heading(doc, "3.2.3. Xử lý giá trị không hợp lệ (Invalid Values)", 3)
    add_body_p(doc, "Kiểm tra các ràng buộc logic tự nhiên của miền bài toán:")
    add_bullet_p(doc, "Kiểm tra giới hạn sinh lý: glucose > 0, HbA1c trong ngưỡng [3.0, 15.0], tuổi > 0. Biến gender ghi nhận 18 bản ghi nhãn 'Other' (<0.02%), được bảo lưu hợp lệ để mô hình hóa trường hợp đặc biệt.", bold_prefix="Tiểu đường: ")
    add_bullet_p(doc, "Kiểm tra ràng buộc vật lý: Diện tích sàn Area > 0, số phòng ngủ/phòng tắm ≥ 1, giá nhà Price > 0, số tầng Stories ≥ 1. Không phát hiện bất kỳ giá trị âm hoặc vô lý nào.", bold_prefix="Giá nhà: ")
    add_bullet_p(doc, "Loại bỏ cột chỉ mục kỹ thuật vô nghĩa Unnamed: 0 phát sinh trong quá trình lưu trữ CSV.", bold_prefix="E-Commerce: ")

    add_styled_heading(doc, "3.2.4. Phân tích ngoại lệ (Outlier Analysis)", 3)
    add_body_p(doc, "Ngoại lệ (Outlier) là các giá trị cách xa phần lớn các quan sát còn lại. Phương pháp phổ biến nhất để phát hiện ngoại lệ trên biến liên tục là dựa trên Khoảng tứ phân vị (Interquartile Range - IQR):")
    add_code_block(doc,
"IQR = Q3 - Q1\n"
"Ngưỡng dưới = Q1 - 1.5 × IQR\n"
"Ngưỡng trên  = Q3 + 1.5 × IQR\n"
"Điểm x được coi là Outlier nếu: x < Ngưỡng dưới  hoặc  x > Ngưỡng trên"
    )
    add_body_p(doc, "Trong bài toán giá nhà, kiểm tra Skewness cho thấy phân bố giá nhà gần như đối xứng hoàn hảo (Skewness = -0.005 ≈ 0). 7 giá trị ngoại lệ xuất hiện ở phân khúc biệt thự cao cấp ($2M+) được bảo lưu nguyên vẹn, vì đây là giao dịch bất động sản thật và việc loại bỏ chúng sẽ làm mất khả năng học các phân khúc nhà cao cấp của mô hình.")

    add_styled_heading(doc, "3.3. Mã hóa biến phân loại", 2)
    add_body_p(doc, "Toàn bộ các biến danh mục được đưa vào OneHotEncoder với cấu hình chuẩn mực: drop='first' và handle_unknown='ignore'.")
    add_bullet_p(doc, "Triệt tiêu hoàn toàn sự phụ thuộc tuyến tính giữa các cột chỉ thị, ngăn ngừa hiện tượng đa cộng tuyến hoàn hảo làm suy biến nghiệm hồi quy tuyến tính.", bold_prefix="drop='first': ")
    add_bullet_p(doc, "Khi hệ thống vận hành thực tế gặp một giá trị nhãn danh mục mới chưa từng xuất hiện trong tập Train, pipeline sẽ tự động gán tất cả các cột dummy về 0 thay vì làm ứng dụng bị văng lỗi ngoại lệ (Crash).", bold_prefix="handle_unknown='ignore': ")

    add_styled_heading(doc, "3.4. Chuẩn hóa dữ liệu số (StandardScaler)", 2)
    add_body_p(doc, "Chuẩn hóa Z-score (StandardScaler) được áp dụng cho toàn bộ các thuộc tính số học liên tục theo công thức:")
    add_code_block(doc,
"z = (x - μ) / σ"
    )
    add_body_p(doc, "Phép biến đổi này đưa dữ liệu về dạng có giá trị trung bình μ = 0 và độ lệch chuẩn σ = 1. Lợi ích kỹ thuật vượt trội: Giúp thuật toán tối ưu hóa Gradient Descent hội tụ nhanh gấp nhiều lần, và bảo đảm hàm khoảng cách Euclid trong các mô hình nhạy cảm thang đo (KNN, SVM) không bị lấn át bởi các thuộc tính có độ lớn số học hàng chục nghìn.")

    add_styled_heading(doc, "3.5. Chia tập dữ liệu: Train, Validation và Test", 2)
    add_body_p(doc, "Để đảm bảo quy chuẩn đánh giá khoa học khách quan và chống hiện tượng quá khớp (Overfitting), tập dữ liệu bắt buộc phải được chia thành 3 phần độc lập:")
    add_bullet_p(doc, "Chiếm 70% tổng dữ liệu. Dùng duy nhất cho thuật toán học các tham số mô hình (Weights, Biases, Cây quyết định).", bold_prefix="Tập Huấn luyện (Train Set): ")
    add_bullet_p(doc, "Chiếm 15% tổng dữ liệu. Dùng để tinh chỉnh siêu tham số (Hyperparameters) và so sánh, lựa chọn mô hình xuất sắc nhất.", bold_prefix="Tập Thẩm định (Validation Set): ")
    add_bullet_p(doc, "Chiếm 15% tổng dữ liệu. Được niêm phong hoàn toàn trong suốt quá trình thử nghiệm. Chỉ được nạp ra đánh giá ĐÚNG MỘT LẦN DUY NHẤT sau khi đã chốt mô hình cuối cùng, đóng vai trò đo lường năng lực tổng quát hóa thực tế.", bold_prefix="Tập Kiểm thử (Test Set): ")
    add_body_p(doc, "Đối với các bài toán có sự mất cân bằng lớp (như Diabetes với nhãn 91.5% vs 8.5%), tùy chọn stratify=y bắt buộc phải được kích hoạt để đảm bảo tỷ lệ nhãn giữa 3 tập là giống hệt nhau.")

    add_styled_heading(doc, "3.6. Ngăn ngừa rò rỉ dữ liệu (Data Leakage Prevention)", 2)
    add_body_p(doc, "Quy trình chuẩn hóa và mã hóa dữ liệu phải tuân thủ nghiêm ngặt nguyên tắc một chiều:")
    add_code_block(doc,
"┌─────────────────────────────────────────────────────────────┐\n"
"│ DỮ LIỆU THÔ BAN ĐẦU                                         │\n"
"└──────────────────────────────┬──────────────────────────────┘\n"
"                               │ Chia tập Train / Val / Test TRƯỚC\n"
"                               ▼\n"
"┌──────────────────────────────┬──────────────────────────────┐\n"
"│ Tập Train (70%)              │ Tập Val (15%) & Test (15%)   │\n"
"├──────────────────────────────┼──────────────────────────────┤\n"
"│ • GỌI scaler.fit(X_train)    │ • TUYỆT ĐỐI KHÔNG GỌI fit()  │\n"
"│ • GỌI encoder.fit(X_train)   │ • CHỈ GỌI transform(X_val)   │\n"
"│ • GỌI tfidf.fit(X_train)     │ • CHỈ GỌI transform(X_test)  │\n"
"└──────────────────────────────┴──────────────────────────────┘"
    )

    add_styled_heading(doc, "3.7. Pipeline tiền xử lý với ColumnTransformer", 2)
    add_body_p(doc, "Để tự động hóa hoàn toàn quy trình trên và đóng gói gọn gàng, Scikit-Learn cung cấp công cụ ColumnTransformer. Công cụ này cho phép định nghĩa các đường ống con độc lập cho từng nhóm cột:")
    add_code_block(doc,
"from sklearn.compose import ColumnTransformer\n"
"from sklearn.preprocessing import StandardScaler, OneHotEncoder\n\n"
"preprocessor = ColumnTransformer(\n"
"    transformers=[\n"
"        ('num', StandardScaler(), num_columns),\n"
"        ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), cat_columns)\n"
"    ]\n"
")"
    )

    add_styled_heading(doc, "3.8. Nguyên tắc tái lập quá trình tiền xử lý (Reproducibility)", 2)
    add_body_p(doc, "Một hệ thống thông minh chỉ được coi là hoàn thiện khi có khả năng tái lập kết quả 100%. Điều này đạt được thông qua: cố định tham số ngẫu nhiên random_state=42 tại mọi bước phân tách và huấn luyện; khóa chặt phiên bản các thư viện trong requirements.txt; và lưu trữ toàn bộ tham số đã fit của ColumnTransformer vào tệp nhị phân duy nhất.")
