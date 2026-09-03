# -*- coding: utf-8 -*-
"""
Chapter II: Theoretical Foundations of Data Representation
"""

from .config import (
    add_styled_heading, add_body_p, add_bullet_p, add_code_block, add_styled_table
)

def build_chapter_2(doc):
    add_styled_heading(doc, "CHƯƠNG II. CƠ SỞ LÝ THUYẾT VỀ BIỂU DIỄN DỮ LIỆU", 1)

    add_styled_heading(doc, "2.1. Tổng quan về học máy và hệ thống thông minh", 2)
    add_body_p(doc, "Học máy (Machine Learning) là một phân ngành của trí tuệ nhân tạo tập trung vào việc phát triển các thuật toán có khả năng tự động rút trích quy luật, mô hình hóa mối quan hệ phức tạp và cải thiện hiệu năng giải quyết tác vụ thông qua việc tiếp cận dữ liệu kinh nghiệm, mà không cần phải lập trình tường minh từng quy tắc rẽ nhánh cố định. Trong một hệ thống thông minh, mô hình học máy đóng vai trò là khối xử lý trung tâm (Inference Engine), biến đổi các thông tin quan sát đầu vào thành các dự báo hoặc quyết định hành động tối ưu.")
    add_body_p(doc, "Tuy nhiên, máy tính số học về bản chất chỉ có thể thực hiện các phép toán đại số tuyến tính: cộng vector, nhân ma trận, tính tích vô hướng và tối ưu hóa vi phân. Các thực thể trong thế giới thực — dù là một bệnh nhân với các triệu chứng lâm sàng, một ngôi nhà với tiện nghi nội thất, hay một bình luận cảm xúc của người tiêu dùng — đều không phải là những con số. Do đó, 'Biểu diễn Dữ liệu' (Data Representation) là bước tiên quyết định hình nên toàn bộ không gian hình học mà tại đó các thuật toán học máy sẽ tìm kiếm ranh giới phân tách hoặc hàm hồi quy xấp xỉ.")

    add_styled_heading(doc, "2.2. Bài toán phân loại và hồi quy", 2)
    add_body_p(doc, "Trong học máy có giám sát (Supervised Learning), tập dữ liệu huấn luyện bao gồm các cặp mẫu (x_i, y_i), trong đó x_i là vector đặc trưng mô tả đối tượng và y_i là nhãn mục tiêu cần dự đoán. Tùy thuộc vào không gian giá trị của y_i, bài toán được phân chia thành hai loại hình cơ bản:")

    add_styled_heading(doc, "2.2.1. Bài toán Phân loại (Classification)", 3)
    add_body_p(doc, "Biến mục tiêu nhận các giá trị rời rạc trong một tập hữu hạn các nhãn lớp: y ∈ {c_1, c_2, ..., c_K}. Khi K = 2, bài toán được gọi là phân loại nhị phân (Binary Classification). Mục tiêu là ước lượng xác suất hậu nghiệm P(y = 1 | x) và vạch ra siêu phẳng phân định (Decision Boundary) trong không gian d chiều.")
    add_body_p(doc, "Trong mô hình tuyến tính phân lớp (Logistic Regression), đầu ra tuyến tính z = w^T x + b được ánh xạ qua hàm kích hoạt phi tuyến Sigmoid (Logistic Function) để chuyển thành xác suất liên tục trong khoảng (0, 1):")
    add_code_block(doc,
"σ(z) = 1 / (1 + e^(-z))    với z = w_1·x_1 + w_2·x_2 + ... + w_d·x_d + b\n\n"
"Quy tắc quyết định:\n"
"  ŷ = 1  nếu P(y=1 | x) = σ(z) ≥ θ  (ngưỡng phân loại chuẩn θ = 0.5)\n"
"  ŷ = 0  nếu P(y=1 | x) = σ(z) < θ"
    )
    add_body_p(doc, "Hàm mất mát được tối ưu hóa trong quá trình huấn luyện là hàm mất mát Entropy chéo nhị phân (Binary Cross-Entropy Loss):")
    add_code_block(doc,
"L(w, b) = - (1/N) × Σ [ y_i · ln(ŷ_i) + (1 - y_i) · ln(1 - ŷ_i) ]"
    )
    add_body_p(doc, "Hàm mất mát này phạt rất nặng khi mô hình đưa ra dự đoán xác suất tự tin nhưng sai lệch nhãn thực tế (ví dụ y=1 nhưng ŷ → 0 thì ln(ŷ) → -∞).")

    add_styled_heading(doc, "2.2.2. Bài toán Hồi quy (Regression)", 3)
    add_body_p(doc, "Biến mục tiêu nhận giá trị liên tục trong tập số thực: y ∈ ℝ (ví dụ giá bán bất động sản bằng USD, nhiệt độ môi trường, huyết áp). Mục tiêu là học hàm ánh xạ f: ℝ^d → ℝ sao cho khoảng cách giữa giá trị dự đoán ŷ_i = f(x_i) và giá trị thực tế y_i là nhỏ nhất trên toàn bộ tập dữ liệu.")
    add_body_p(doc, "Trong hồi quy tuyến tính cổ điển (Linear Regression), hàm giả thuyết có dạng:")
    add_code_block(doc,
"ŷ = w^T x + b = w_1·x_1 + w_2·x_2 + ... + w_d·x_d + b"
    )
    add_body_p(doc, "Hàm mất mát tối ưu hóa phổ biến nhất là Tổng bình phương sai số (Ordinary Least Squares - OLS) hay Sai số bình phương trung bình (Mean Squared Error - MSE):")
    add_code_block(doc,
"L_MSE(w, b) = (1/N) × Σ (y_i - ŷ_i)² = (1/N) × Σ (y_i - (w^T x_i + b))²"
    )

    add_styled_heading(doc, "2.3. Khái niệm biểu diễn dữ liệu", 2)
    add_body_p(doc, "Biểu diễn dữ liệu là quá trình chuyển hóa thông tin thô, đa dạng từ thế giới thực (văn bản nhận xét, thông số bệnh án, vị trí địa lý) thành các cấu trúc đại số có thể tính toán được. Mỗi cách biểu diễn phản ánh một góc nhìn hình học khác nhau về dữ liệu. Một phép biểu diễn tốt phải bảo tồn tối đa các thông tin đặc trưng có ý nghĩa phân tách (Discriminative Features), đồng thời triệt tiêu nhiễu và bảo đảm tính nhất quán toán học.")

    add_styled_heading(doc, "2.4. Vectơ đặc trưng (Feature Vector)", 2)
    add_body_p(doc, "Một đối tượng quan sát thứ i được số hóa thành một vector cột d chiều trong không gian số thực ℝ^d:")
    add_code_block(doc,
"x_i = [x_{i1}, x_{i2}, ..., x_{id}]^T  ∈  ℝ^d"
    )
    add_body_p(doc, "Mỗi phần tử x_{ij} đại diện cho tọa độ của đối tượng trên trục đặc trưng thứ j. Số chiều d của vector phản ánh mức độ chi tiết của không gian mô tả.")
    add_body_p(doc, "Ví dụ thực tế từ bài toán Tiểu đường: Một bệnh nhân nam, 55 tuổi, chỉ số BMI = 28.5 kg/m², mức HbA1c = 6.8%, Glucose = 155 mg/dL, không có tiền sử tăng huyết áp hay bệnh tim, chưa từng hút thuốc. Sau khi đi qua bộ biến đổi ColumnTransformer (chuẩn hóa Z-score các biến số và mã hóa One-Hot biến danh mục), vector đặc trưng số học 13 chiều có dạng cụ thể:", bold_prefix="Ví dụ minh họa: ")
    add_code_block(doc,
"# Giả sử giá trị trung bình và độ lệch chuẩn của tập Train:\n"
"# age: μ=41.89, σ=22.52 → z_age = (55 - 41.89) / 22.52 ≈ 0.582\n"
"# bmi: μ=27.32, σ=6.64   → z_bmi = (28.5 - 27.32) / 6.64  ≈ 0.178\n"
"# HbA1c: μ=5.53, σ=1.07  → z_hba1c = (6.8 - 5.53) / 1.07 ≈ 1.187\n"
"# glucose: μ=138.06, σ=40.71 → z_glucose = (155 - 138.06) / 40.71 ≈ 0.416\n"
"# hypertension = 0, heart_disease = 0\n"
"# gender_Male = 1, gender_Other = 0 (bỏ Female)\n"
"# smoke_current=0, smoke_ever=0, smoke_former=0, smoke_never=1, smoke_not_current=0\n\n"
"x_i = [0.582, 0.178, 1.187, 0.416, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]^T ∈ ℝ^13"
    )

    add_styled_heading(doc, "2.5. Ma trận đặc trưng (Feature Matrix)", 2)
    add_body_p(doc, "Khi tập hợp N quan sát độc lập, ta xếp các vector đặc trưng chuyển vị x_i^T thành các hàng kế tiếp nhau để tạo thành Ma trận đặc trưng toàn cục X:")
    add_code_block(doc,
"X = [ x_1^T ]     [ x_{11}  x_{12}  ...  x_{1d} ]\n"
"    [ x_2^T ]  =  [ x_{21}  x_{22}  ...  x_{2d} ]   ∈  ℝ^(N × d)\n"
"    [  ...  ]     [  ...     ...    ...   ...   ]\n"
"    [ x_N^T ]     [ x_{N1}  x_{N2}  ...  x_{Nd} ]"
    )
    add_body_p(doc, "Ý nghĩa của hai chiều trong ma trận đặc trưng:")
    add_bullet_p(doc, "Chiều dòng thứ nhất (N - Samples): Đại diện cho số lượng quan sát/mẫu độc lập trong tập dữ liệu. Mỗi dòng chứa toàn bộ thông tin của đúng một thực thể duy nhất.", bold_prefix="Chiều dòng (N): ")
    add_bullet_p(doc, "Chiều cột thứ hai (d - Features): Đại diện cho số chiều của không gian đặc trưng sau khi đã hoàn tất các phép biến đổi toán học. Mỗi cột tương ứng với một thuộc tính cụ thể.", bold_prefix="Chiều cột (d): ")
    add_styled_table(
        doc,
        "Bảng 2.1. Tổng hợp kích thước ma trận đặc trưng qua các tập phân chia của ba ứng dụng",
        ["Ứng dụng", "Số chiều (d)", "Tập Train (X_train)", "Tập Val (X_val)", "Tập Test (X_test)"],
        [
            ["Diabetes Prediction", "d = 13", "ℝ^(67,302 × 13)", "ℝ^(14,422 × 13)", "ℝ^(14,422 × 13)"],
            ["House Price Prediction", "d = 23", "ℝ^(1,400 × 23)", "ℝ^(300 × 23)", "ℝ^(300 × 23)"],
            ["E-Commerce Combined", "d = 2,532", "ℝ^(16,440 × 2,532)", "ℝ^(3,523 × 2,532)", "ℝ^(3,523 × 2,532)"]
        ],
        col_widths=[1.8, 1.0, 1.4, 1.4, 1.4]
    )

    add_styled_heading(doc, "2.6. Tensor và biểu diễn dữ liệu nhiều chiều", 2)
    add_body_p(doc, "Trong đại số đa tuyến tính, Tensor là sự tổng quát hóa của đại lượng vô hướng (Scalar - Tensor hạng 0), vector (Tensor hạng 1) và ma trận (Tensor hạng 2) lên các không gian n chiều bất kỳ. Trong khi dữ liệu dạng bảng được mô tả đầy đủ bằng ma trận 2 chiều ℝ^(N × d), các miền dữ liệu phức tạp hơn đòi hỏi cấu trúc Tensor bậc cao:")
    add_bullet_p(doc, "Được biểu diễn dưới dạng Tensor 3 chiều ℝ^(B × T × d), trong đó B là kích thước lô (Batch Size), T là độ dài chuỗi từ tối đa trong câu, và d là số chiều của vector nhúng từ (Embedding Dimension).", bold_prefix="Dữ liệu chuỗi ngôn ngữ / Thời gian: ")
    add_bullet_p(doc, "Được biểu diễn dưới dạng Tensor 4 chiều ℝ^(B × C × H × W), trong đó C là số kênh màu (Channel = 3 với ảnh RGB), H là chiều cao điểm ảnh, và W là chiều rộng điểm ảnh.", bold_prefix="Dữ liệu hình ảnh (Computer Vision): ")

    add_styled_heading(doc, "2.7. Biểu diễn dữ liệu văn bản: TF-IDF vs Dense Embedding", 2)
    add_body_p(doc, "Ngôn ngữ tự nhiên là dạng dữ liệu phi cấu trúc phức tạp. Để đưa văn bản vào các thuật toán học máy, cần phân biệt rạch ròi hai trường phái biểu diễn cơ bản theo bài giảng Lecture 02:")

    add_styled_heading(doc, "2.7.1. Biểu diễn túi từ thống kê (TF-IDF Vector — Sử dụng trong Assignment 02)", 3)
    add_body_p(doc, "Phương pháp Túi từ (Bag-of-Words - BoW) và trọng số TF-IDF (Term Frequency - Inverse Document Frequency) biến đổi mỗi văn bản thành một vector thưa (sparse vector) trong không gian từ vựng cố định V có kích thước d = |V|:")
    add_code_block(doc,
"TF(t, d) = f_{t,d} / Σ_{t' ∈ d} f_{t',d}      (Tần suất xuất hiện của từ t trong văn bản d)\n\n"
"IDF(t, D) = ln[ (1 + |D|) / (1 + |{d ∈ D : t ∈ d}|) ] + 1   (Nghịch đảo tần suất tài liệu)\n\n"
"TF-IDF(t, d) = TF(t, d) × IDF(t, D)"
    )
    add_body_p(doc, "Vector TF-IDF sau đó được chuẩn hóa theo chuẩn L2 (Euclidean Norm) để độ dài vector bằng 1, giúp loại bỏ ảnh hưởng của độ dài văn bản ngắn hay dài:")
    add_code_block(doc,
"v_{norm} = v / ||v||_2 = v / √(Σ v_i²)"
    )
    add_body_p(doc, "Đặc điểm bản chất: TF-IDF tạo ra vector THƯA (sparse) với phần lớn các chiều mang giá trị 0. Số chiều rất lớn (trong dự án d_text = 2,500). TF-IDF HOÀN TOÀN KHÔNG PHẢI VECTOR NHÚNG (Embedding) và không thể hiện được tính tương đồng ngữ nghĩa: hai từ đồng nghĩa như 'beautiful' và 'gorgeous' là hai trục tọa độ trực giao độc lập.")

    add_styled_heading(doc, "2.7.2. Biểu diễn nhúng sâu (Dense Embedding Vectors — Bài giảng Lecture 02)", 3)
    add_body_p(doc, "Khác với TF-IDF, phương pháp biểu diễn nhúng từ sâu (Word / Sentence Embeddings) chuyển đổi văn bản thông qua ba giai đoạn liên tục:")
    add_code_block(doc,
"Raw Text ──> Tokenization ──> Token IDs (Chỉ số nguyên) ──> Embedding Lookup ──> Dense Vectors"
    )
    add_bullet_p(doc, "Là các số nguyên không âm duy nhất đại diện cho chỉ số của từ hoặc mảnh từ trong từ điển từ vựng (Vocabulary). Ví dụ câu 'I love this dress' được tách thành các token ID: [42, 1892, 19, 452]. Token ID thuần túy là con trỏ chỉ mục, không mang ý nghĩa số học đại số.", bold_prefix="Token IDs: ")
    add_bullet_p(doc, "Token ID được dùng để tra cứu (Lookup) trong Ma trận nhúng W_embed ∈ ℝ^(|V| × d_embed). Kết quả thu được là một vector ĐẶC (Dense Vector) số chiều thấp (thường d = 64 đến 768), nơi các giá trị là số thực phân bố liên tục.", bold_prefix="Embedding Vectors: ")
    add_body_p(doc, "Trong không gian nhúng liên tục, khoảng cách góc Cosine (Cosine Similarity) phản ánh chính xác sự tương đồng ngữ nghĩa: cos(v['beautiful'], v['gorgeous']) ≈ 0.88 rất gần 1. Báo cáo khẳng định rõ: Dự án Assignment 02 sử dụng TF-IDF thưa, không sử dụng Dense Embedding.")

    add_styled_table(
        doc,
        "Bảng 2.2. So sánh toàn diện giữa Biểu diễn TF-IDF thưa và Biểu diễn Dense Embedding",
        ["Tiêu chí so sánh", "Biểu diễn túi từ TF-IDF", "Biểu diễn Dense Embedding (Lecture 02)"],
        [
            ["Bản chất toán học", "Vector thưa (Sparse Vector)", "Vector đặc (Dense Vector)"],
            ["Số chiều không gian (d)", "Rất lớn (d = 1,000 – 100,000)", "Thấp đến trung bình (d = 64 – 768)"],
            ["Quan hệ ngữ nghĩa từ", "Trực giao (không biểu diễn từ đồng nghĩa)", "Liên tục (từ đồng nghĩa có khoảng cách gần)"],
            ["Trật tự từ ngữ trong câu", "Bị phá vỡ hoàn toàn (Bag-of-Words)", "Bảo tồn qua thứ tự token / Positional Encoding"],
            ["Phương pháp tính toán", "Đếm tần suất thống kê thuần túy", "Học qua mạng nơ-ron sâu (Word2Vec, Transformer)"],
            ["Mô hình phù hợp", "Logistic Regression, LinearSVM, Naive Bayes", "MLP, RNN, LSTM, Transformer, BERT"]
        ],
        col_widths=[1.5, 2.7, 2.7]
    )

    add_styled_heading(doc, "2.8. Mã hóa dữ liệu phân loại", 2)
    add_body_p(doc, "Các biến phân loại chuỗi ký tự (như giới tính, tình trạng nội thất, thành phố) không thể đưa trực tiếp vào các phép tính nhân vô hướng. Có hai phương pháp mã hóa chính:")
    add_bullet_p(doc, "Gán mỗi nhãn danh mục với một số nguyên: ví dụ {Unfurnished: 0, Semi-Furnished: 1, Furnished: 2}. Phương pháp này chỉ phù hợp với biến có quan hệ thứ bậc tự nhiên (Ordinal Variables). Nếu áp dụng cho biến danh nghĩa vô hướng (Nominal) như City (Mumbai=1, Delhi=2, Chennai=3), thuật toán sẽ vô tình coi Delhi gấp đôi Mumbai, dẫn tới sai lệch nghiệm toán học nghiêm trọng.", bold_prefix="Label Encoding: ")
    add_bullet_p(doc, "Tạo ra các cột nhị phân chỉ thị (dummy columns) cho từng giá trị danh mục. Để loại bỏ hiện tượng đa cộng tuyến hoàn hảo (Dummy Variable Trap — khi một cột có thể suy diễn hoàn toàn từ tổ hợp tuyến tính của các cột khác), tùy chọn drop='first' luôn được kích hoạt.", bold_prefix="One-Hot Encoding: ")

    add_styled_heading(doc, "2.9. Kiểu dữ liệu và miền giá trị", 2)
    add_body_p(doc, "Việc phân định rạch ròi kiểu dữ liệu số học (liên tục hay rời rạc) và miền giá trị (thang đo, biên độ) quyết định chiến lược tiền xử lý. Ví dụ: biến số liên tục có biên độ lớn (diện tích 1,000 - 15,000 sq ft) bắt buộc phải qua StandardScaler, trong khi các biến chỉ thị nhị phân {0, 1} đã có sẵn thang đo chuẩn hóa tự nhiên.")

    add_styled_heading(doc, "2.10. Tính nhất quán của biểu diễn dữ liệu", 2)
    add_body_p(doc, "Một nguyên lý bất biến trong kỹ nghệ học máy: Quy trình biểu diễn dữ liệu áp dụng cho tập huấn luyện (Train) bắt buộc phải được áp dụng hoàn toàn nhất quán trên dữ liệu kiểm thử (Test) và dữ liệu suy luận thực tế (Production Inference). Nếu tại thời điểm huấn luyện, thuộc tính age được chuẩn hóa bằng trung bình μ_train và độ lệch chuẩn σ_train, thì tại thời điểm người dùng gửi request từ Web Client, giá trị age đầu vào cũng phải được chuẩn hóa bằng đúng μ_train và σ_train đó. Đây là lý do kiến trúc Pipeline nguyên khối là yêu cầu bắt buộc.")

    add_styled_heading(doc, "2.11. Rò rỉ dữ liệu (Data Leakage)", 2)
    add_body_p(doc, "Rò rỉ dữ liệu là hiện tượng thông tin từ tập kiểm thử (Test) hoặc tập thẩm định (Validation) bị rò rỉ vào quá trình huấn luyện mô hình, khiến mô hình đạt điểm số cao giả tạo nhưng thất bại hoàn toàn khi triển khai thực tế. Nguyên nhân phổ biến nhất là tính toán các tham số thống kê (μ, σ, giá trị điền khuyết thiếu trung vị, từ điển TF-IDF) trên toàn bộ dữ liệu trước khi phân chia tập. Nguyên tắc vàng để triệt tiêu Data Leakage: Luôn phân chia tập Train / Validation / Test trước, và CHỈ GỌI .fit() trên tập Train.")
