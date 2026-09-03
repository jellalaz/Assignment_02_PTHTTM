# -*- coding: utf-8 -*-
"""
Chapter IV: Evaluation Metrics for Machine Learning Models
"""

from .config import (
    add_styled_heading, add_body_p, add_bullet_p, add_code_block, add_styled_table
)

def build_chapter_4(doc):
    add_styled_heading(doc, "CHƯƠNG IV. CÁC ĐỘ ĐO ĐÁNH GIÁ MÔ HÌNH", 1)

    add_styled_heading(doc, "4.1. Đối với bài toán Hồi quy (Regression)", 2)
    add_body_p(doc, "Trong bài toán hồi quy, mục tiêu là đo lường mức độ sai lệch giữa vector giá trị thực tế y = [y_1, ..., y_N]^T và vector giá trị dự đoán ŷ = [ŷ_1, ..., ŷ_N]^T. Bốn chỉ số cơ bản được sử dụng đồng thời:")

    add_styled_heading(doc, "4.1.1. Sai số tuyệt đối trung bình (Mean Absolute Error - MAE)", 3)
    add_code_block(doc,
"MAE = (1/N) × Σ_{i=1}^N |y_i - ŷ_i|"
    )
    add_body_p(doc, "Ưu điểm vượt trội của MAE là mang cùng đơn vị đo vật lý với biến mục tiêu (ví dụ đơn vị USD trong dự đoán giá nhà). MAE đo lường sai số bình quân trên mỗi giao dịch mà không khuếch đại các ngoại lệ, giúp các chuyên gia kinh doanh và khách hàng dễ dàng hiểu được độ tin cậy của mô hình.")

    add_styled_heading(doc, "4.1.2. Sai số bình phương trung bình (MSE) và Căn bậc hai (RMSE)", 3)
    add_code_block(doc,
"MSE = (1/N) × Σ_{i=1}^N (y_i - ŷ_i)²\n\n"
"RMSE = √MSE = √[ (1/N) × Σ_{i=1}^N (y_i - ŷ_i)² ]"
    )
    add_body_p(doc, "Do có phép bình phương trước khi lấy trung bình, MSE và RMSE phạt rất nặng các lỗi dự đoán sai lệch lớn. Nếu RMSE lớn hơn đáng kể so với MAE, điều đó chứng tỏ mô hình đang gặp phải một số trường hợp dự đoán sai lệch cực đoan.")

    add_styled_heading(doc, "4.1.3. Hệ số xác định (Coefficient of Determination - R² Score)", 3)
    add_code_block(doc,
"R² = 1 - [ SS_res / SS_tot ] = 1 - [ Σ_{i=1}^N (y_i - ŷ_i)² / Σ_{i=1}^N (y_i - ȳ)² ]\n"
"trong đó ȳ = (1/N) × Σ_{i=1}^N y_i là giá trị trung bình mẫu thực tế."
    )
    add_body_p(doc, "R² thể hiện tỷ lệ phần trăm phương sai của biến mục tiêu được giải thích bởi các biến độc lập trong mô hình. Một mô hình hoàn hảo đạt R² = 1.0; một mô hình Baseline luôn đoán giá trị trung bình ȳ đạt R² = 0.0; và mô hình dự đoán tệ hơn cả Baseline sẽ có R² âm.")

    add_styled_heading(doc, "4.2. Đối với bài toán Phân lớp (Classification)", 2)
    add_body_p(doc, "Đối với bài toán phân loại, việc đánh giá dựa trên Ma trận nhầm lẫn (Confusion Matrix) và các độ đo chuyên biệt:")

    add_styled_heading(doc, "4.2.1. Ma trận nhầm lẫn (Confusion Matrix)", 3)
    add_styled_table(
        doc,
        "Bảng 4.1. Cấu trúc chuẩn của Ma trận nhầm lẫn (Confusion Matrix) trong phân loại nhị phân",
        ["Thực tế \\ Dự đoán", "Dự đoán Lớp Âm (Pred = 0)", "Dự đoán Lớp Dương (Pred = 1)"],
        [
            ["Thực tế Lớp Âm (Actual = 0)", "True Negative (TN)\n(Dự đoán đúng người khỏe mạnh)", "False Positive (FP - Lỗi Loại I)\n(Báo động nhầm người khỏe thành bệnh)"],
            ["Thực tế Lớp Dương (Actual = 1)", "False Negative (FN - Lỗi Loại II)\n(Bỏ sót ca bệnh hiểm nghèo)", "True Positive (TP)\n(Phát hiện đúng ca mắc bệnh)"]
        ],
        col_widths=[2.0, 2.5, 2.5]
    )

    add_styled_heading(doc, "4.2.2. Các chỉ số phân lớp: Accuracy, Precision, Recall và F1-Score", 3)
    add_code_block(doc,
"Accuracy  = (TP + TN) / (TP + TN + FP + FN)\n"
"Precision = TP / (TP + FP)       (Độ chuẩn xác trong số ca dự đoán dương)\n"
"Recall    = TP / (TP + FN)       (Độ nhạy - Khả năng bắt trúng các ca dương thực tế)\n"
"F1-Score  = 2 × (Precision × Recall) / (Precision + Recall)"
    )
    add_body_p(doc, "Sự vô nghĩa của Accuracy trên dữ liệu mất cân bằng: Trong tập dữ liệu Diabetes (87,976 mẫu âm vs 8,170 mẫu dương — tỷ lệ 91.5% vs 8.5%), một mô hình tầm thường luôn luôn dự đoán mọi người đều Không mắc bệnh (Negative) vẫn sẽ đạt Accuracy = 91.5%! Tuy nhiên, mô hình này hoàn toàn vô dụng và cực kỳ nguy hiểm trong y tế vì có Recall = 0% (bỏ sót 100% bệnh nhân).", bold_prefix="Cảnh báo kỹ thuật: ")
    add_body_p(doc, "Chi phí của Lỗi Loại I (FP) so với Lỗi Loại II (FN): Trong y tế dự phòng, chi phí của một ca FN là tính mạng con người — bệnh nhân mắc bệnh tiểu đường nhưng bị báo nhầm là khỏe mạnh, dẫn tới không được can thiệp điều trị và phát triển biến chứng suy thận, đột quỵ. Ngược lại, chi phí của một ca FP chỉ là việc bệnh nhân thực hiện thêm một xét nghiệm khẳng định lại. Do đó, RECALL LÀ CHỈ SỐ TỐI THƯỢNG.")

    add_styled_heading(doc, "4.2.3. Đường cong ROC và Chỉ số ROC-AUC", 3)
    add_body_p(doc, "Đường cong ROC (Receiver Operating Characteristic) thể hiện sự biến thiên giữa Tỷ lệ dương tính thật (TPR = Recall) và Tỷ lệ dương tính giả (FPR = FP / (FP + TN)) khi ngưỡng quyết định θ thay đổi liên tục từ 0 đến 1. Chỉ số ROC-AUC (Area Under the Curve) đo lường diện tích dưới đường cong này, phản ánh xác suất mà mô hình xếp hạng một mẫu dương tính cao hơn một mẫu âm tính ngẫu nhiên. Mô hình đoán mò đạt AUC = 0.5, mô hình hoàn hảo đạt AUC = 1.0.")
