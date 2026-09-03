# -*- coding: utf-8 -*-
"""
Chapter VIII: Application 2 — House Price Prediction
"""

from docx.enum.text import WD_ALIGN_PARAGRAPH
from .config import (
    add_styled_heading, add_body_p, add_bullet_p, add_code_block, add_code_snippet_with_notes,
    add_styled_table, add_figure_with_notes
)

def build_chapter_8(doc):
    add_styled_heading(doc, "CHƯƠNG VIII. ỨNG DỤNG 2 — DỰ ĐOÁN GIÁ NHÀ", 1)

    add_styled_heading(doc, "8.1. Mô tả bài toán", 2)
    add_body_p(doc, "Định giá bất động sản nhà ở là một bài toán kinh tế then chốt, giữ vai trò quyết định trong việc hỗ trợ người mua, người bán, các tổ chức tín dụng thẩm định thế chấp và cơ quan thuế xác định giá trị thị trường công bằng. Tuy nhiên, giá trị của một ngôi nhà chịu tác động đồng thời của vô số yếu tố phi đồng nhất: từ quy mô diện tích sàn, số lượng phòng ngủ/phòng tắm, tuổi thọ công trình cho đến vị trí địa lý đắc địa và các tiện ích hạ tầng đi kèm.")
    add_body_p(doc, "Mục tiêu của ứng dụng là xây dựng một hệ thống hồi quy học máy có khả năng ước lượng tự động giá trị thị trường của bất động sản nhà ở (tính theo USD) dựa trên các thông số đặc tả kỹ thuật. Đây là bài toán hồi quy giá trị liên tục (Continuous Regression):")
    add_bullet_p(doc, "Tập hợp 15 đặc trưng mô tả ngôi nhà bao gồm 7 biến số liên tục/rời rạc và 8 biến danh mục.", bold_prefix="Tập đặc trưng đầu vào (X): ")
    add_bullet_p(doc, "Giá bán thực tế của bất động sản tính bằng đơn vị Dollar Mỹ (USD).", bold_prefix="Biến mục tiêu (y = Price): ")

    add_styled_heading(doc, "8.2. Giới thiệu tập dữ liệu", 2)
    add_body_p(doc, "Hệ thống sử dụng tập dữ liệu bất động sản thực tế từ nền tảng Kaggle: 'House Price Prediction Dataset (2000 rows)' do tác giả chershi công bố. Link dataset: https://www.kaggle.com/datasets/chershi/house-price-prediction-dataset-2000-rows. Tập dữ liệu bao gồm chính xác 2,000 bản ghi giao dịch nhà đất thực tế với 16 cột thuộc tính chi tiết.")
    add_code_block(doc,
">>> df = pd.read_csv('data/raw/house_price/house_price_prediction_dataset.csv')\n"
">>> df.shape\n"
"(2000, 16)\n\n"
">>> df.head(3)\n"
"   Area  Bedrooms  Bathrooms  Stories  Parking  Age  Locality Rating      City  \\\n"
"0  2100         3          2        2        1   12                7    Mumbai   \n"
"1  3500         4          3        2        2    5                9     Delhi   \n"
"2  1200         2          1        1        0   25                4  Bangalore   \n\n"
"      Furnishing Main Road Guest Room Basement Water Supply Air Conditioning \\\n"
"0      Furnished       Yes         No       No  Corporation              Yes   \n"
"1  Semi-Furnished       Yes        Yes      Yes         Both              Yes   \n"
"2    Unfurnished        No         No       No  Corporation               No   \n\n"
"  Preferred Tenant    Price\n"
"0           Family  1450000\n"
"1          Company  1820000\n"
"2        Bachelor    850000"
    )

    add_styled_heading(doc, "8.3. Khảo sát và tìm hiểu dữ liệu", 2)
    add_body_p(doc, "Tập dữ liệu bao gồm 8 thuộc tính dạng số và 8 thuộc tính dạng chuỗi danh mục:")
    add_styled_table(
        doc,
        "Bảng 8.1. Danh mục các thuộc tính của tập dữ liệu House Price Prediction",
        ["Thuộc tính", "Phân loại", "Miền giá trị", "Ý nghĩa trong định giá bất động sản"],
        [
            ["Area", "Numerical", "1,000 – 15,000 sq ft", "Tổng diện tích mặt sàn sử dụng của ngôi nhà"],
            ["Bedrooms / Bathrooms", "Numerical", "1 – 5 phòng", "Số lượng phòng ngủ và phòng tắm vệ sinh"],
            ["Stories / Parking", "Numerical", "1 – 4 tầng; 0 – 3 xe", "Số tầng cao của công trình và sức chứa chỗ đỗ xe"],
            ["Age", "Numerical", "0 – 80 năm", "Tuổi thọ của công trình tính từ năm hoàn công"],
            ["Locality Rating", "Numerical", "1 – 10 điểm", "Điểm số đánh giá chất lượng vị trí, hạ tầng khu vực"],
            ["City", "Categorical", "Chennai, Delhi, Mumbai...", "Thành phố tọa lạc (7 đô thị lớn)"],
            ["Furnishing", "Categorical", "Furnished, Semi, Unfurnished", "Tình trạng nội thất bàn giao"],
            ["Main Road / Air Conditioning", "Categorical", "Yes / No", "Nhà mặt tiền đường chính và trang bị điều hòa"],
            ["Guest Room / Basement", "Categorical", "Yes / No", "Có phòng cho khách và có tầng hầm chứa đồ"],
            ["Water Supply / Preferred Tenant", "Categorical", "Corporation, Both; Family...", "Nguồn cấp nước sạch và nhóm đối tượng thuê ưu tiên"],
            ["Price (Target)", "Target (Numerical)", "$334,635 – $2,225,409", "Giá trị thị trường thực tế của bất động sản (USD)"]
        ],
        col_widths=[1.6, 1.1, 1.4, 2.5],
        align_cols=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    )

    add_styled_heading(doc, "8.4. Làm sạch dữ liệu", 2)
    add_body_p(doc, "Khảo sát tính toàn vẹn khẳng định tập dữ liệu đạt chất lượng hoàn hảo: 0 giá trị khuyết thiếu (df.isnull().sum() = 0 trên cả 16 cột) và 0 bản ghi trùng lặp (df.duplicated().sum() = 0).")
    add_body_p(doc, "Phân tích độ lệch (Skewness Analysis) trên biến mục tiêu Price và các biến số:")
    add_code_block(doc,
">>> df['Price'].skew()\n"
"-0.004797   # Độ lệch xấp xỉ bằng 0 tuyệt đối!\n\n"
">>> df[['Area', 'Age', 'Locality Rating']].skew()\n"
"Area              -0.001205\n"
"Age                0.048395\n"
"Locality Rating    0.055934"
    )
    add_body_p(doc, "Do hệ số Skewness của Price xấp xỉ 0, phân bố giá nhà mang tính đối xứng chuẩn mực hình chuông Gauss hoàn hảo (Mean = $1,245,014.50 và Median = $1,246,602.00 gần như trùng khít). Do đó, việc giữ nguyên đơn vị USD tự nhiên để huấn luyện mà không áp dụng phép biến đổi log-transform là hoàn toàn chuẩn xác về mặt toán học, giúp giữ nguyên ý nghĩa tiền tệ thực tế cho chỉ số sai số MAE.")

    add_styled_heading(doc, "8.5. Biểu diễn dữ liệu", 2)
    add_body_p(doc, "Không gian vector đặc trưng được tạo lập thông qua ColumnTransformer:")
    add_bullet_p(doc, "Gồm 7 biến: Area, Bedrooms, Bathrooms, Stories, Parking, Age, Locality Rating → Áp dụng StandardScaler → 7 chiều số thực.", bold_prefix="Đặc trưng số học (7 chiều): ")
    add_bullet_p(doc, "Gồm 8 biến: City (7 giá trị → 6 cột dummy sau khi drop first), Furnishing (3 giá trị → 2 cột dummy) và 6 biến nhị phân Yes/No (mỗi biến 1 cột dummy) → Áp dụng OneHotEncoder(drop='first') → 16 chiều nhị phân.", bold_prefix="Đặc trưng danh mục (16 chiều): ")
    add_body_p(doc, "Tổng số chiều không gian đặc trưng là: d = 7 + 16 = 23 chiều. Kích thước ma trận huấn luyện và kiểm thử:")
    add_code_block(doc,
"x_i ∈ ℝ^23\n"
"X_train ∈ ℝ^(1,400 × 23),   X_val ∈ ℝ^(300 × 23),   X_test ∈ ℝ^(300 × 23)"
    )

    add_styled_heading(doc, "8.6. Phân tích khám phá dữ liệu (EDA)", 2)
    add_body_p(doc, "Bốn đồ thị phân tích sâu sắc mối tương quan kinh tế giữa các thuộc tính:")


    code_house_dist = '''# Vẽ phân bố giá bán (Histogram + KDE)
plt.figure(figsize=(8, 5))
sns.histplot(df['Price'], bins=50, kde=True, color='skyblue')
plt.title("Phân bố Giá bán Bất động sản (House Price Distribution)")
plt.xlabel("Giá bán")
plt.ylabel("Tần suất")
plt.tight_layout()
plt.show()'''

    add_code_snippet_with_notes(
        doc,
        code_text=code_house_dist,
        caption_text="Đoạn mã 8.3. Trực quan hóa phân bố biến liên tục bằng Histogram và đường KDE.",
        description_items=[
            "Sử dụng sns.histplot kết hợp tham số kde=True để vẽ biểu đồ phân bố tần suất và đường cong mật độ ước lượng.",
            "Đoạn mã giúp phát hiện hiện tượng phân bố lệch phải (Right-skewed) của giá nhà, từ đó hiểu rõ hơn về đặc tính dữ liệu thị trường thực tế."
        ],
        source_file="notebooks/02_house_price.ipynb"
    )

    add_figure_with_notes(
        doc,
        "figures/house_price/price_distribution.png",

        "Hình 8.1. Phân bố giá trị bất động sản (Price) trong tập dữ liệu.",
        [
            "Đồ thị tần số và đường cong mật độ thể hiện dạng chuông chuẩn mực hình chuông Gauss.",
            "Giá trị dao động từ $334,635 đến $2,225,409, tập trung chủ yếu quanh mức $1.2M – $1.3M."
        ],
        explanation="Tập dữ liệu đã được tổng hợp cân đối trên các phân khúc thị trường bất động sản.",
        ml_implication="Hàm mất mát bình phương tối thiểu (MSE/RMSE) hoạt động ở trạng thái tối ưu nhất trên phân bố đối xứng chuẩn mà không bị kéo lệch bởi các đuôi ngoại lệ."
    )

    add_figure_with_notes(
        doc,
        "figures/house_price/area_locality_vs_price.png",
        "Hình 8.2. Mối quan hệ giữa Diện tích (Area), Đánh giá vị trí (Locality) và Giá nhà.",
        [
            "Đồ thị phân tán thể hiện xu hướng tuyến tính đi lên rất rõ ràng giữa Diện tích sàn và Giá nhà.",
            "Điểm đánh giá vị trí (Locality Rating từ 1 đến 10) đóng vai trò nâng đỡ mức giá nền tảng: Cùng một diện tích, các ngôi nhà có vị trí đắc địa (màu đậm) có giá cao hơn rõ rệt."
        ],
        explanation="Vị trí và quy mô diện tích là hai thành tố cấu thành cốt lõi nhất của giá trị đất và nhà ở.",
        ml_implication="Mối quan hệ mang tính cộng tuyến tính mạnh, là cơ sở vững chắc cho các mô hình hồi quy tuyến tính và hồi quy sườn núi (Ridge)."
    )

    add_figure_with_notes(
        doc,
        "figures/house_price/rooms_vs_price.png",
        "Hình 8.3. Mối quan hệ giữa Số phòng ngủ, Số phòng tắm và Giá nhà.",
        [
            "Số lượng phòng ngủ (Bedrooms từ 1 đến 5) và phòng tắm (Bathrooms) tỷ lệ thuận với mức giá trung bình của bất động sản.",
            "Sự gia tăng phòng tắm mang lại bước nhảy giá trị lớn hơn so với phòng ngủ, phản ánh mức độ tiện nghi cao cấp của căn nhà."
        ],
        explanation="Nhiều phòng tắm đòi hỏi hạ tầng đường ống và thiết bị vệ sinh đắt tiền, đại diện cho phân khúc nhà cao cấp.",
        ml_implication="Các thuộc tính số nguyên rời rạc này cung cấp tín hiệu phân bậc rất tốt cho mô hình hồi quy."
    )

    add_figure_with_notes(
        doc,
        "figures/house_price/correlation_heatmap.png",
        "Hình 8.4. Ma trận tương quan giữa các thuộc tính đặc trưng và giá nhà.",
        [
            "Diện tích (Area) là thuộc tính có tương quan tuyến tính cao nhất với giá nhà (r = 0.58).",
            "Kế tiếp là Đánh giá vị trí (r = 0.35), Số phòng tắm (r = 0.31), Số phòng ngủ (r = 0.28) và Chỗ đỗ xe (r = 0.26).",
            "Tuổi thọ công trình (Age) có tương quan âm với giá nhà (r = -0.19), nhà càng cũ thì giá trị khấu hao càng lớn."
        ],
        explanation="Hệ số tương quan phản ánh hoàn toàn chính xác các quy luật định giá bất động sản thực tế.",
        ml_implication="Các đặc trưng đều có đóng góp tích cực vào việc giải thích phương sai của mô hình hồi quy."
    )

    add_styled_heading(doc, "8.7. Xây dựng mô hình", 2)
    add_body_p(doc, "Tập dữ liệu 2,000 bản ghi được phân chia ngẫu nhiên thành: 1,400 mẫu Train (70%), 300 mẫu Validation (15%) và 300 mẫu Test (15%). Mô hình cơ sở DummyRegressor (dự đoán trung vị) được đem đối đầu cùng 5 thuật toán hồi quy.")

    add_styled_heading(doc, "8.8. Đánh giá mô hình", 2)
    add_styled_table(
        doc,
        "Bảng 8.2. So sánh hiệu năng các mô hình hồi quy trên tập Validation",
        ["Mô hình", "MAE ($)", "MSE", "RMSE ($)", "R² Score", "Thời gian (s)"],
        [
            ["Dummy Baseline (Median)", "241,302.3", "91,389,000,000", "302,306.1", "-0.0003", "0.01s"],
            ["Linear Regression", "125,450.1", "23,466,700,000", "153,188.5", "0.7431", "0.02s"],
            ["Ridge Regression (α=1.0)", "125,436.7", "23,468,100,000", "153,193.0", "0.7431", "0.02s"],
            ["Decision Tree Regressor", "197,822.6", "59,022,500,000", "242,945.5", "0.3540", "0.02s"],
            ["Random Forest Regressor", "148,108.1", "34,524,300,000", "185,807.2", "0.6221", "0.13s"],
            ["Gradient Boosting Regressor", "135,629.0", "28,949,300,000", "170,145.1", "0.6831", "0.19s"]
        ],
        col_widths=[1.8, 1.0, 1.2, 1.0, 0.8, 1.0],
        align_cols=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER]
    )

    add_figure_with_notes(
        doc,
        "figures/house_price/model_comparison.png",
        "Hình 8.5. So sánh sai số và hệ số R² giữa các mô hình hồi quy trên tập Validation.",
        [
            "Hai mô hình tuyến tính (Linear Regression và Ridge Regression) đạt hiệu năng cao nhất, giải thích được hơn 74.3% phương sai dữ liệu (R² = 0.7431) và giảm sai số MAE xuống chỉ còn ~$125,436.",
            "Các mô hình phi tuyến tính dựa trên cây (Decision Tree và Random Forest) đạt kết quả kém hơn rõ rệt (Decision Tree chỉ đạt R² = 0.3540)."
        ],
        explanation="Bản chất định giá nhà là tổng hòa của các yếu tố cộng gộp (Diện tích × đơn giá + Tiện nghi × chi phí). Mô hình cây bị hiện tượng phân mảnh vùng dữ liệu (Discretization Error) và không ngoại suy mượt mà được hàm liên tục như mô hình tuyến tính.",
        ml_implication="Không phải lúc nào mô hình phức tạp cũng tốt hơn. Cần chọn mô hình phù hợp với bản chất toán học của dữ liệu."
    )

    add_figure_with_notes(
        doc,
        "figures/house_price/actual_vs_predicted_residuals.png",
        "Hình 8.6. Đồ thị Giá thực tế so với Giá dự đoán và Phân bố phần dư (Residuals) trên tập Test.",
        [
            "Các điểm dự đoán trên đồ thị phân tán bám rất sát đường chéo lý tưởng y = ŷ trải dài từ phân khúc $400k đến $2.2M.",
            "Đồ thị phân bố phần dư (Residuals) hội tụ đối xứng quanh giá trị 0, không xuất hiện hiện tượng phương sai thay đổi (Heteroscedasticity)."
        ],
        explanation="Mô hình dự đoán công bằng trên cả phân khúc nhà giá thấp, trung bình và biệt thự cao cấp.",
        ml_implication="Đảm bảo tính vững chắc và khả năng tổng quát hóa đáng tin cậy khi đưa vào thực tế."
    )

    add_styled_heading(doc, "8.9. Lựa chọn mô hình", 2)
    add_body_p(doc, "Mô hình Ridge Regression (α = 1.0) được lựa chọn chính thức để đóng gói triển khai. Cơ chế phạt trọng số L2 giúp triệt tiêu hoàn toàn sự bất ổn định hệ số do đa cộng tuyến giữa các thuộc tính tiện nghi nhà. Kết quả kiểm định trên tập Test 300 căn nhà độc lập:")
    add_styled_table(
        doc,
        "Bảng 8.3. Kết quả kiểm định mô hình Ridge Regression trên tập Test độc lập",
        ["Chỉ số hồi quy", "Giá trị thực nghiệm", "Ý nghĩa kinh tế"],
        [
            ["MAE (Sai số tuyệt đối)", "$126,793.85", "Sai lệch bình quân ~10% so với giá trị trung bình $1.2M"],
            ["RMSE (Căn bậc hai MSE)", "$154,661.80", "Đo lường mức độ phạt các sai số lớn"],
            ["R² Score (Hệ số xác định)", "0.7448 (74.48%)", "Mô hình giải thích thành công 74.48% biến thiên giá thị trường"]
        ],
        col_widths=[2.0, 1.8, 2.8]
    )

    add_styled_heading(doc, "8.10. Triển khai hệ thống", 2)

    add_figure_with_notes(
        doc,
        "screenshots/api/api_house_result.png",
        "Hình 8.7. Kết quả gọi API định giá bất động sản (/predict/house) trên Swagger UI.",
        [
            "Request gửi thông số căn nhà: Area=2500, Bedrooms=3, Bathrooms=2, City=Mumbai, Furnishing=Furnished...",
            "API phản hồi dự đoán định giá thị trường: $1,446,747.88, thời gian tính toán < 5ms."
        ],
        explanation="Pipeline tự động chuẩn hóa Z-score và tạo 23 chiều đặc trưng để Ridge Regression tính tích vô hướng w^T x + b.",
        ml_implication="Hỗ trợ tích hợp mượt mà vào các sàn giao dịch bất động sản trực tuyến."
    )

    add_figure_with_notes(
        doc,
        "screenshots/web/house_web_result.png",
        "Hình 8.8. Kết quả định giá bất động sản trên giao diện Web Desktop.",
        [
            "Giao diện hiển thị trực quan mức giá ước tính bằng USD có định dạng dấu phẩy ngăn cách hàng nghìn rõ ràng.",
            "Cung cấp khoảng tin cậy tham chiếu cho khách hàng."
        ],
        explanation="Hiển thị trực quan thân thiện với người dùng cá nhân.",
        ml_implication="Hỗ trợ người mua nhà có ngay cơ sở thương lượng giá với bên môi giới."
    )

    add_figure_with_notes(
        doc,
        "screenshots/mobile/house_mobile.png",
        "Hình 8.9. Giao diện định giá bất động sản trên thiết bị di động truy cập qua mạng LAN (Smartphone Viewport).",
        [
            "Môi giới bất động sản có thể đứng ngay tại ngôi nhà thực tế, dùng điện thoại nhập thông số và nhận định giá ngay lập tức.",
            "Bố cục form co giãn mượt mà trên khung nhìn hẹp của smartphone."
        ],
        explanation="Tận dụng kết nối mạng LAN để phục vụ tính toán di động tức thì.",
        ml_implication="Nâng cao năng suất làm việc tại hiện trường của đội ngũ tư vấn bất động sản.",
        max_width_inches=3.2
    )
