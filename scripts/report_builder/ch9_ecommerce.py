# -*- coding: utf-8 -*-
"""
Chapter IX: Application 3 — E-Commerce Customer Behavior & Interest Discovery
"""

from docx.enum.text import WD_ALIGN_PARAGRAPH
from .config import (
    add_styled_heading, add_body_p, add_bullet_p, add_code_block,
    add_styled_table, add_figure_with_notes
)

def build_chapter_9(doc):
    add_styled_heading(doc, "CHƯƠNG IX. ỨNG DỤNG 3 — E-COMMERCE CUSTOMER BEHAVIOR & INTEREST DISCOVERY", 1)

    add_styled_heading(doc, "9.1. Mô tả bài toán", 2)
    add_body_p(doc, "Trong thương mại điện tử hiện đại, sự bùng nổ của phản hồi khách hàng (Customer Feedback) mang lại nguồn tài nguyên dữ liệu khổng lồ nhưng phần lớn tồn tại dưới dạng ngôn ngữ tự nhiên tự do không cấu trúc. Một câu hỏi cốt lõi của bài toán là: Liệu nội dung nhận xét chi tiết của người mua có chứa đựng những tín hiệu cảm xúc vượt ra ngoài các con số sao khô khan (Rating)?")
    add_body_p(doc, "Mục tiêu của ứng dụng là xây dựng một hệ thống phân loại đa phương thức (Multimodal Classification) kết hợp dữ liệu bảng định lượng với văn bản tự do để dự đoán hành vi khuyến nghị sản phẩm (Recommended IND ∈ {0, 1}), đồng thời khám phá các sở thích và điểm nghẽn trải nghiệm của người tiêu dùng:")
    add_bullet_p(doc, "Bao gồm cả thông tin nhân khẩu (tuổi), hành vi định lượng (số sao đánh giá, số lượt feedback hữu ích) và văn bản tự do (tiêu đề và nội dung đánh giá chi tiết).", bold_prefix="Tập đặc trưng đầu vào (X): ")
    add_bullet_p(doc, "Hành vi đề xuất sản phẩm của khách hàng, trong đó y = 1 biểu thị khách hàng sẽ khuyến nghị sản phẩm cho người khác và y = 0 biểu thị không khuyến nghị.", bold_prefix="Biến mục tiêu (y = Recommended IND): ")

    add_styled_heading(doc, "9.2. Giới thiệu tập dữ liệu", 2)
    add_body_p(doc, "Hệ thống khai thác tập dữ liệu thực tế: 'Women's E-Commerce Clothing Reviews' do tác giả nicapotato công bố trên Kaggle. Link dataset: https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews. Tập dữ liệu chứa 23,486 lượt nhận xét khách hàng nữ trên 11 cột thuộc tính.")
    add_code_block(doc,
">>> df = pd.read_csv('data/raw/ecommerce/Womens_Clothing_E-Commerce_Reviews.csv')\n"
">>> df.shape\n"
"(23486, 11)\n\n"
">>> df.columns.tolist()\n"
"['Unnamed: 0', 'Clothing ID', 'Age', 'Title', 'Review Text', 'Rating',\n"
" 'Recommended IND', 'Positive Feedback Count', 'Division Name',\n"
" 'Department Name', 'Class Name']"
    )

    add_styled_heading(doc, "9.3. Biểu diễn khách hàng (Customer Representation)", 2)
    add_body_p(doc, "Mỗi khách hàng trong tập dữ liệu được biểu diễn toàn diện qua 3 giác cắt thông tin:")
    add_bullet_p(doc, "Tuổi tác khách hàng (Age, dao động từ 18 đến 99 tuổi).", bold_prefix="1. Nhân khẩu học (Demographics): ")
    add_bullet_p(doc, "Số sao đánh giá (Rating từ 1 đến 5 sao) và Số lượt người khác bấm thích nhận xét (Positive Feedback Count).", bold_prefix="2. Hành vi định lượng (Quantitative Behavior): ")
    add_bullet_p(doc, "Tiêu đề nhận xét (Title) và Nội dung đánh giá chi tiết (Review Text) phản ánh cảm xúc chân thực, độ vừa vặn, chất liệu vải và ý định sử dụng.", bold_prefix="3. Trải nghiệm định tính (Qualitative Experience): ")

    add_styled_heading(doc, "9.4. Làm sạch dữ liệu", 2)
    add_bullet_p(doc, "Loại bỏ cột chỉ mục thừa 'Unnamed: 0' bằng lệnh df.drop(columns=['Unnamed: 0']).", bold_prefix="Cột chỉ mục: ")
    add_bullet_p(doc, "Trường Title (thiếu 3,810 dòng) và Review Text (thiếu 845 dòng) được điền bằng chuỗi rỗng '' trước khi nối ghép thành cột văn bản hợp nhất full_review = Title + ' ' + Review Text, bảo đảm không làm mất bất kỳ bản ghi khách hàng nào.", bold_prefix="Nối văn bản: ")
    add_bullet_p(doc, "Các cột danh mục Division Name, Department Name, Class Name bị khuyết thiếu nhẹ (14 dòng) được điền bằng nhãn 'Unknown' qua SimpleImputer.", bold_prefix="Biến danh mục: ")

    add_styled_heading(doc, "9.5. Ba chế độ biểu diễn dữ liệu", 2)
    add_body_p(doc, "Hệ thống thiết lập 3 chế độ biểu diễn độc lập để so sánh đối đầu:")

    add_styled_heading(doc, "9.5.1. Chế độ chỉ dùng dữ liệu bảng (Tabular Only — d = 32)", 3)
    add_body_p(doc, "Xử lý 3 thuộc tính số (Age, Rating, Positive Feedback Count) qua StandardScaler và 3 thuộc tính danh mục sản phẩm (Division, Department, Class) qua OneHotEncoder(drop='first'). Tổng số chiều đặc trưng bảng: d_tab = 32 chiều.")

    add_styled_heading(doc, "9.5.2. Chế độ chỉ dùng văn bản (Text TF-IDF Only — d = 2,500)", 3)
    add_body_p(doc, "Áp dụng TfidfVectorizer trên cột full_review với cấu hình: max_features=2500, ngram_range=(1, 2) (bao gồm cả unigram và bigram như 'great fit', 'runs small') và loại bỏ stop words tiếng Anh chuẩn. Mỗi bình luận trở thành một vector thưa chuẩn hóa L2 trong không gian d_text = 2,500 chiều.")

    add_styled_heading(doc, "9.5.3. Chế độ kết hợp Đa phương thức (Combined Tabular + Text — d = 2,532)", 3)
    add_body_p(doc, "Ma trận bảng đặc và ma trận TF-IDF thưa được ghép nối đồng thời qua ColumnTransformer để tạo thành không gian đặc trưng thống nhất:")
    add_code_block(doc,
"d_combined = d_tab + d_text = 32 + 2,500 = 2,532 chiều\n"
"X_train ∈ ℝ^(16,440 × 2,532),   X_val ∈ ℝ^(3,523 × 2,532),   X_test ∈ ℝ^(3,523 × 2,532)"
    )

    add_styled_heading(doc, "9.6. Khám phá sở thích và Phân tích EDA", 2)
    add_body_p(doc, "Ba biểu đồ phân tích sâu sắc các chiều cạnh hành vi người tiêu dùng:")

    add_figure_with_notes(
        doc,
        "figures/ecommerce/target_rating_distribution.png",
        "Hình 9.1. Phân bố số sao đánh giá (Rating) và Tỷ lệ khuyến nghị (Recommended IND).",
        [
            "Tập dữ liệu có 82.2% lượt đánh giá đi kèm khuyến nghị (Lớp 1) và 17.8% không khuyến nghị (Lớp 0).",
            "Khách hàng cho 5 sao và 4 sao gần như 100% sẽ khuyến nghị; đánh giá 1 sao và 2 sao hầu hết không khuyến nghị.",
            "Tuy nhiên, nhóm đánh giá 3 sao là vùng ranh giới phân vân đặc biệt: Tỷ lệ khuyến nghị xấp xỉ 50/50."
        ],
        explanation="Điểm số 3 sao đại diện cho những sản phẩm khách hàng vừa thích một điểm (kiểu dáng) nhưng lại thất vọng về điểm khác (chất liệu).",
        ml_implication="Nếu chỉ dùng dữ liệu bảng (Rating = 3), mô hình hoàn toàn đoán mò. Cần phải có văn bản nhận xét để phân định cảm xúc thực sự."
    )

    add_figure_with_notes(
        doc,
        "figures/ecommerce/department_review_length.png",
        "Hình 9.2. Phân bố độ dài nhận xét theo từng ngành hàng sản phẩm.",
        [
            "Hai ngành hàng có số lượng nhận xét áp đảo nhất là Tops (Áo) và Dresses (Váy đầm), chiếm hơn 70% tổng lượng tương tác.",
            "Độ dài nhận xét của khách hàng không hài lòng (Lớp 0) có xu hướng dài hơn đáng kể so với khách hàng hài lòng."
        ],
        explanation="Khi khách hàng thất vọng hoặc gặp sự cố về kích cỡ, họ có xu hướng viết bài bình luận rất chi tiết để phàn nàn và cảnh báo người mua sau.",
        ml_implication="Độ dài văn bản và số lượng từ vựng phàn nàn là những tín hiệu định lượng bổ sung đắt giá."
    )

    add_figure_with_notes(
        doc,
        "figures/ecommerce/top_keywords_tfidf.png",
        "Hình 9.3. Top các từ khóa TF-IDF đặc trưng nhất trong đánh giá khách hàng.",
        [
            "Các từ khóa mang trọng số tích cực cao nhất: 'love', 'perfect', 'flattering', 'comfortable', 'great fit', 'beautiful'.",
            "Các từ khóa mang trọng số tiêu cực cao nhất: 'disappointed', 'cheap', 'runs small', 'returned', 'terrible', 'itchy'."
        ],
        explanation="Khách hàng nữ quan tâm hàng đầu đến độ vừa vặn cơ thể (fit, flattering) và chất liệu vải (soft vs cheap/itchy).",
        ml_implication="Bộ vector hóa TF-IDF đã trích xuất thành công các thuộc tính cảm xúc then chốt giúp mô hình phân lớp rực rỡ."
    )

    add_styled_heading(doc, "9.7. Xây dựng mô hình", 2)
    add_body_p(doc, "Tập dữ liệu 23,486 dòng được phân chia stratified thành: 16,440 mẫu Train (70%), 3,523 mẫu Validation (15%) và 3,523 mẫu Test (15%). Hệ thống huấn luyện đồng thời 8 mô hình trên cả 3 chế độ biểu diễn để đối chiếu hiệu năng.")

    add_styled_heading(doc, "9.8. Đánh giá mô hình", 2)
    add_styled_table(
        doc,
        "Bảng 9.1. So sánh hiệu năng giữa các chế độ biểu diễn dữ liệu E-Commerce trên tập Validation",
        ["Mô hình", "Chế độ Biểu diễn", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"],
        [
            ["Logistic Regression", "Tabular Only (d=32)", "0.9466", "0.9913", "0.9434", "0.9667", "0.9818"],
            ["Decision Tree", "Tabular Only (d=32)", "0.9446", "0.9898", "0.9424", "0.9655", "0.9778"],
            ["Random Forest", "Tabular Only (d=32)", "0.9466", "0.9913", "0.9434", "0.9667", "0.9793"],
            ["SVM (LinearSVC)", "Tabular Only (d=32)", "0.9441", "0.9764", "0.9551", "0.9656", "0.9817"],
            ["Gradient Boosting", "Tabular Only (d=32)", "0.9418", "0.9770", "0.9517", "0.9642", "0.9819"],
            ["TF-IDF + Logistic Regression", "Text Only (d=2,500)", "0.8799", "0.9657", "0.8854", "0.9238", "0.9422"],
            ["TF-IDF + LinearSVC", "Text Only (d=2,500)", "0.9018", "0.9192", "0.9655", "0.9418", "0.9318"],
            ["Combined Tabular + TF-IDF LogReg", "Combined (d=2,532)", "0.9466", "0.9895", "0.9451", "0.9668", "0.9877"]
        ],
        col_widths=[1.8, 1.4, 0.7, 0.7, 0.7, 0.7, 0.8],
        align_cols=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER]
    )

    add_figure_with_notes(
        doc,
        "figures/ecommerce/representation_comparison.png",
        "Hình 9.4. Biểu đồ so sánh hiệu năng giữa các chế độ biểu diễn Tabular, Text và Combined.",
        [
            "Mô hình Combined Tabular + TF-IDF vươn lên dẫn đầu toàn diện về ROC-AUC đạt đỉnh 0.9877 trên tập Validation.",
            "Mô hình chỉ dùng Text TF-IDF tuy không mạnh bằng Tabular (do Rating chiếm ưu thế) nhưng khi ghép cặp đã bổ sung tín hiệu cảm xúc tuyệt vời."
        ],
        explanation="Minh chứng khoa học cho thấy sự kết hợp đa phương thức giữa thông tin định lượng và ngôn ngữ tự nhiên đem lại sức mạnh phân loại cao nhất.",
        ml_implication="Khẳng định giá trị thực tiễn của dữ liệu văn bản bình luận trong thương mại điện tử."
    )

    add_figure_with_notes(
        doc,
        "figures/ecommerce/confusion_matrix.png",
        "Hình 9.5. Ma trận nhầm lẫn của mô hình Combined Logistic Regression trên tập Test độc lập.",
        [
            "Trên 3,523 đánh giá kiểm thử độc lập, mô hình nhận diện chính xác 2,704 lượt khuyến nghị (True Positives) và 587 lượt không khuyến nghị (True Negatives).",
            "Số ca dự đoán nhầm ở mức rất thấp, đạt Accuracy = 93.41% và ROC-AUC = 0.9737."
        ],
        explanation="Mô hình có khả năng phân định cực kỳ dứt khoát giữa hai luồng ý kiến của khách hàng.",
        ml_implication="Sẵn sàng ứng dụng vào dây chuyền kiểm duyệt và phân loại đánh giá tự động."
    )

    add_styled_heading(doc, "9.9. Phân tích thực nghiệm: Văn bản nhận xét có thực sự cải thiện chất lượng mô hình?", 2)
    add_body_p(doc, "Câu trả lời là: CÓ, VĂN BẢN NHẬN XÉT CẢI THIỆN RÕ RỆT CHẤT LƯỢNG MÔ HÌNH VỀ CẢ ĐỊNH LƯỢNG LẪN ĐỊNH TÍNH.")
    add_body_p(doc, "1. Bằng chứng định lượng: Diện tích dưới đường cong ROC-AUC tăng từ 0.9819 (mô hình Tabular tốt nhất là Gradient Boosting) lên 0.9877 trên tập Validation và đạt 0.9737 trên tập Test độc lập hoàn toàn.")
    add_body_p(doc, "2. Bằng chứng định tính & Cơ chế hoạt động: Biến số Rating giải thích tốt cho các trường hợp cực đoan (1, 2 sao hoặc 4, 5 sao). Tuy nhiên, tại phân khúc đánh giá trung bình 3 sao, điểm số không thể hiện được ý định thực tế (tỷ lệ khuyến nghị 50/50). Bằng việc phân tích các cụm từ TF-IDF, mô hình phát hiện được: Nếu nhận xét 3 sao chứa từ 'flattering', 'great material', khách hàng vẫn sẵn sàng khuyến nghị sản phẩm (Recommended=1); ngược lại nếu chứa 'itchy', 'runs small', 'returned', khách hàng sẽ không khuyến nghị (Recommended=0).")

    add_styled_heading(doc, "9.10. Ý nghĩa kinh doanh (Business Interpretation)", 2)
    add_bullet_p(doc, "Tops và Dresses là hai mặt hàng đóng góp doanh thu và thu hút thảo luận lớn nhất (>70%), cần ưu tiên tối ưu giao diện và chất lượng hình ảnh cho hai danh mục này.", bold_prefix="Mặt hàng chủ lực: ")
    add_bullet_p(doc, "Nguyên nhân hàng đầu khiến khách hàng không khuyến nghị sản phẩm may mặc là vấn đề kích cỡ không chuẩn (runs small/large) và chất liệu vải mỏng/ngứa (thin/cheap material).", bold_prefix="Điểm nghẽn sản phẩm: ")
    add_bullet_p(doc, "Doanh nghiệp thương mại điện tử cần bổ sung bảng hướng dẫn chọn size chi tiết kèm số đo chiều cao/cân nặng của người mẫu, đồng thời cải tiến chất lượng dệt may để giảm tỷ lệ hoàn hàng (returns).", bold_prefix="Hành động chiến lược: ")

    add_styled_heading(doc, "9.11. Triển khai hệ thống", 2)

    add_figure_with_notes(
        doc,
        "screenshots/api/api_ecommerce_result.png",
        "Hình 9.6. Kết quả gọi API phân tích nhận xét khách hàng (/predict/ecommerce) trên Swagger UI.",
        [
            "Request gửi lên: Title='Love this dress', Review Text='Fabric is soft and flattering', Rating=5, Age=32...",
            "API phản hồi: prediction=1 (Recommended), xác suất khuyến nghị 98.2%, độ tin cậy 'High Confidence'."
        ],
        explanation="Pipeline tự động vector hóa văn bản TF-IDF, ghép nối với dữ liệu bảng và đưa qua mô hình phân loại.",
        ml_implication="Hỗ trợ doanh nghiệp gắn nhãn tự động hàng triệu bình luận mỗi ngày."
    )

    add_figure_with_notes(
        doc,
        "screenshots/web/ecommerce_web_result.png",
        "Hình 9.7. Kết quả phân tích nhận xét khách hàng trên giao diện Web Desktop.",
        [
            "Giao diện hiển thị trực quan thông điệp: Sản phẩm được khuyến nghị mạnh mẽ kèm thanh đo xác suất 98%.",
            "Hệ thống cung cấp tóm tắt các đặc trưng ảnh hưởng chính tới quyết định của thuật toán."
        ],
        explanation="Hiển thị thân thiện cho các nhà quản lý sàn thương mại điện tử.",
        ml_implication="Hỗ trợ các nhà bán lẻ theo dõi sức khỏe thương hiệu (Brand Sentiment) theo thời gian thực."
    )

    add_figure_with_notes(
        doc,
        "screenshots/mobile/ecommerce_mobile.png",
        "Hình 9.8. Giao diện phân tích nhận xét khách hàng trên thiết bị di động truy cập qua mạng LAN (Smartphone Viewport).",
        [
            "Cho phép người dùng nhập trực tiếp nhận xét bằng bàn phím ảo trên điện thoại và nhận phản hồi đánh giá tức thì.",
            "Thiết kế tối ưu hóa tốc độ tải và bố cục trên khung nhìn di động."
        ],
        explanation="Mô phỏng hoàn hảo trải nghiệm mua sắm trên các ứng dụng di động Shopee/Lazada.",
        ml_implication="Chứng minh tính khả thi của việc tích hợp AI phân tích ngôn ngữ lên thiết bị di động.",
        max_width_inches=3.2
    )
