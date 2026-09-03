# -*- coding: utf-8 -*-
"""
Chapter V: Machine Learning Model Construction Methods
"""

from .config import (
    add_styled_heading, add_body_p, add_bullet_p, add_code_block, add_styled_table
)

def build_chapter_5(doc):
    add_styled_heading(doc, "CHƯƠNG V. PHƯƠNG PHÁP XÂY DỰNG MÔ HÌNH", 1)

    add_styled_heading(doc, "5.1. Tổng quan về xây dựng mô hình", 2)
    add_body_p(doc, "Xây dựng mô hình học máy là giai đoạn huấn luyện các thuật toán trên tập dữ liệu Train nhằm tìm ra các tham số tối ưu (trọng số, cây phân nhánh) giúp mô hình có khả năng khái quát hóa tốt nhất trên dữ liệu chưa từng thấy. Để đảm bảo tính khách quan và khoa học, dự án áp dụng chiến lược 'Đua tài mô hình' (Model Benchmarking): huấn luyện đồng thời nhiều họ thuật toán với các giả định toán học khác nhau và đối chiếu trên cùng một tập dữ liệu thẩm định Validation độc lập.")

    add_styled_heading(doc, "5.2. Mô hình Baseline", 2)
    add_body_p(doc, "Mô hình Baseline là điểm tựa tối thiểu để kiểm chứng tính hữu ích của các thuật toán học máy phức tạp:")
    add_bullet_p(doc, "Sử dụng DummyClassifier với chiến lược stratified: Dự đoán ngẫu nhiên theo đúng tỷ lệ phân bố lớp của tập huấn luyện. Một thuật toán học máy chỉ được coi là có giá trị nếu vượt trội rõ rệt so với Baseline này.", bold_prefix="Trong bài toán phân lớp: ")
    add_bullet_p(doc, "Sử dụng DummyRegressor với chiến lược median: Luôn luôn dự đoán giá trị trung vị của biến mục tiêu trong tập Train cho mọi căn nhà.", bold_prefix="Trong bài toán hồi quy: ")

    add_styled_heading(doc, "5.3. Các mô hình cho bài toán hồi quy", 2)
    add_body_p(doc, "Năm thuật toán hồi quy tiêu biểu được triển khai song song cho bài toán định giá bất động sản:")

    add_styled_heading(doc, "5.3.1. Hồi quy tuyến tính cổ điển (Linear Regression OLS)", 3)
    add_body_p(doc, "Phương pháp bình phương tối thiểu thông thường (Ordinary Least Squares - OLS) tìm kiếm vector trọng số w sao cho tổng bình phương sai số dự đoán là nhỏ nhất. Nghiệm giải tích tường minh có dạng: w = (X^T X)^(-1) X^T y. Ưu điểm: Đơn giản, tốc độ tính toán cực nhanh. Nhược điểm: Nhạy cảm với hiện tượng đa cộng tuyến khi ma trận X^T X gần suy biến.")

    add_styled_heading(doc, "5.3.2. Hồi quy sườn núi (Ridge Regression — L2 Regularization)", 3)
    add_body_p(doc, "Bổ sung thành phần phạt chuẩn L2 (L2 Penalty) vào hàm mất mát OLS: L_Ridge = Σ (y_i - w^T x_i)² + α ||w||_2². Nghiệm giải tích: w = (X^T X + α I)^(-1) X^T y. Nhờ việc cộng thêm ma trận đường chéo α I, ma trận nghịch đảo luôn khả nghịch, giúp triệt tiêu hoàn toàn sự dao động hệ số do đa cộng tuyến giữa các thuộc tính tiện nghi nhà.")

    add_styled_heading(doc, "5.3.3. Cây quyết định hồi quy (Decision Tree Regressor)", 3)
    add_body_p(doc, "Phân chia không gian đặc trưng thành các hình siêu hộp chữ nhật đệ quy dựa trên tiêu chí giảm thiểu phương sai (Variance Reduction). Tại mỗi nút lá, giá trị dự đoán là trung bình của các mẫu rơi vào vùng đó. Ưu điểm: Bắt được quan hệ phi tuyến. Nhược điểm: Rất dễ bị quá khớp (overfitting) và không ngoại suy liên tục mượt mà.")

    add_styled_heading(doc, "5.3.4. Rừng ngẫu nhiên hồi quy (Random Forest Regressor)", 3)
    add_body_p(doc, "Tập hợp (Ensemble) 100 cây quyết định độc lập được huấn luyện theo cơ chế Bagging (Bootstrap Aggregating) và ngẫu nhiên hóa đặc trưng. Dự đoán cuối cùng là trung bình cộng đầu ra của toàn bộ 100 cây, giúp giảm thiểu phương sai sai số đáng kể.")

    add_styled_heading(doc, "5.3.5. Tăng cường độ dốc (Gradient Boosting Regressor)", 3)
    add_body_p(doc, "Thuật toán học tập hợp tuần tự (Boosting): Các cây quyết định nông được huấn luyện nối tiếp nhau, trong đó mỗi cây mới tập trung học và bù đắp phần dư sai số (Residuals) của cây đứng trước nó. Đây là một trong những thuật toán hồi quy bảng mạnh mẽ nhất hiện nay.")

    add_styled_heading(doc, "5.4. Các mô hình cho bài toán phân loại", 2)
    add_body_p(doc, "Năm thuật toán phân lớp được triển khai cho bài toán chẩn đoán tiểu đường và bài toán thương mại điện tử:")

    add_styled_heading(doc, "5.4.1. Hồi quy Logistic (Logistic Regression)", 3)
    add_body_p(doc, "Mô hình xác suất tuyến tính ánh xạ tích vô hướng w^T x qua hàm Sigmoid để xuất ra xác suất thuộc lớp 1. Áp dụng tối ưu hóa L-BFGS kết hợp điều chuẩn L2. Điểm mạnh đặc biệt: Tốc độ suy luận siêu tốc (< 1 ms), khả năng diễn giải trọng số trực quan, và xử lý cực tốt các ma trận thưa số chiều lớn (như TF-IDF 2,532 chiều trong bài toán E-Commerce).")

    add_styled_heading(doc, "5.4.2. K láng giềng gần nhất (K-Nearest Neighbors - KNN)", 3)
    add_body_p(doc, "Thuật toán học dựa trên cá thể (Instance-based learning) với k = 5. Khoảng cách giữa các mẫu được tính theo chuẩn Euclid d(x, x') = √(Σ (x_j - x'_j)²). Nhược điểm: Chi phí tính toán tăng tuyến tính theo số mẫu N tại thời điểm dự đoán, và rất nhạy cảm với thang đo biến.")

    add_styled_heading(doc, "5.4.3. Cây quyết định phân lớp (Decision Tree Classifier)", 3)
    add_body_p(doc, "Phân chia không gian dựa trên chỉ số vẩn đục Gini Impurity: Gini = 1 - Σ p_k². Cung cấp khả năng truy vết logic quyết định dưới dạng cây phân nhánh If-Else.")

    add_styled_heading(doc, "5.4.4. Rừng ngẫu nhiên phân lớp (Random Forest Classifier)", 3)
    add_body_p(doc, "Tập hợp 100 cây quyết định phân lớp với cơ chế bầu chọn đa số (Majority Voting). Trong bài toán mất cân bằng nhãn y tế, tham số class_weight='balanced' được kích hoạt để tự động tăng trọng số lỗi phạt của các mẫu thuộc lớp thiểu số (Lớp 1 - mắc bệnh), buộc mô hình phải tập trung học ranh giới bao phủ lớp bệnh.")

    add_styled_heading(doc, "5.4.5. Máy vector hỗ trợ tuyến tính (LinearSVC)", 3)
    add_body_p(doc, "Tìm kiếm siêu phẳng phân tách có độ rộng lề (Margin) cực đại dựa trên hàm mất mát Hinge Loss. Để có thể xuất ra xác suất phục vụ giao diện người dùng, LinearSVC được bọc trong bộ chuẩn hóa CalibratedClassifierCV.")

    add_styled_heading(doc, "5.5. Đóng gói quy trình học máy (Scikit-Learn Pipeline)", 2)
    add_body_p(doc, "Toàn bộ tiền xử lý và mô hình suy luận được tích hợp chặt chẽ vào một đối tượng Pipeline nguyên khối. Bảng sau tổng hợp cấu hình tham số chính thức của các mô hình trong toàn dự án:")
    add_styled_table(
        doc,
        "Bảng 5.1. Bảng tổng hợp cấu hình siêu tham số (Hyperparameters) chính của các mô hình",
        ["Mô hình", "Loại bài toán", "Siêu tham số chính thức", "Mục đích cấu hình"],
        [
            ["Logistic Regression", "Phân lớp", "solver='lbfgs', max_iter=1000, C=1.0", "Hội tụ ổn định trên vector d=2,532"],
            ["KNN", "Phân lớp", "n_neighbors=5, metric='minkowski', p=2", "Số láng giềng k=5 chuẩn"],
            ["Decision Tree", "Phân lớp/Hồi quy", "criterion='gini' / 'squared_error', random_state=42", "Cố định tính tái lập kết quả"],
            ["Random Forest", "Phân lớp", "n_estimators=100, class_weight='balanced'", "Ưu tiên tối thượng độ nhạy Recall"],
            ["LinearSVC", "Phân lớp", "loss='squared_hinge', CalibratedClassifierCV", "Xuất xác suất hậu nghiệm mượt mà"],
            ["Ridge Regression", "Hồi quy", "alpha=1.0, solver='auto'", "Triệt tiêu đa cộng tuyến tiện nghi nhà"],
            ["Gradient Boosting", "Hồi quy", "n_estimators=100, learning_rate=0.1, max_depth=3", "Chống overfitting cây sâu"]
        ],
        col_widths=[1.5, 1.2, 2.2, 2.1]
    )
