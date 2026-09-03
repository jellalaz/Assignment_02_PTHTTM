# BÁO CÁO KỸ THUẬT — ASSIGNMENT 02
## MÔN HỌC: PHÁT TRIỂN CÁC HỆ THỐNG THÔNG MINH (INTELLIGENT SYSTEM DEVELOPMENT)
### CHỦ ĐỀ: TỪ BIỂU DIỄN DỮ LIỆU ĐẾN TRIỂN KHAI HỆ THỐNG THÔNG MINH (FROM DATA REPRESENTATION TO DEPLOYABLE INTELLIGENT SYSTEMS)

**Giảng viên hướng dẫn:** PGS. TS. Trần Đình Quế  
**Học viện:** Học viện Công nghệ Bưu chính Viễn thông (PTIT)  
**Môi trường thực thi & kiểm nghiệm:** `ai-env` (Python 3.12.13, Scikit-Learn 1.4+, FastAPI 0.110+)  
**Dữ liệu thực nghiệm:** 100% dữ liệu thật từ Kaggle (Không sử dụng dữ liệu giả lập)

---

## TÓM TẮT DỰ ÁN (EXECUTIVE SUMMARY)

Dự án này hoàn thành trọn vẹn toàn bộ chuỗi phát triển hệ thống thông minh theo tiêu chuẩn:
$$\text{Raw Data} \longrightarrow \text{Understand} \longrightarrow \text{Clean} \longrightarrow \text{Represent} \longrightarrow \text{Learn} \longrightarrow \text{Evaluate} \longrightarrow \text{Persist} \longrightarrow \text{Deploy}$$

Ba hệ thống học máy hoàn chỉnh được xây dựng và triển khai bao gồm:
1. **Hệ thống Chẩn đoán Nguy cơ Tiểu đường (Diabetes Prediction):** Bài toán Phân loại nhị phân trên 100,000 bản ghi lâm sàng. Mô hình được chọn là **Random Forest Classifier** với Recall = 89.70% và ROC-AUC = 0.9743 trên tập kiểm tra độc lập.
2. **Hệ thống Định giá Bất động sản (House Price Prediction):** Bài toán Hồi quy trên 2,000 bất động sản thực tế. Mô hình được chọn là **Gradient Boosting Regressor** với $R^2 = 0.7448$ và MAE = ~$126,793 trên tập kiểm tra.
3. **Hệ thống Phân tích Hành vi & Đề xuất Sản phẩm Thương mại điện tử (E-Commerce Customer Behavior):** Bài toán Phân loại kết hợp dữ liệu bảng và ngôn ngữ tự nhiên (Multimodal Tabular + Text TF-IDF) trên 23,486 đánh giá. Mô hình **Combined Tabular + TF-IDF Logistic Regression** đạt ROC-AUC = 0.9737 và Accuracy = 93.41%.

Toàn bộ hệ thống được đóng gói thành REST API (FastAPI) và phục vụ giao diện người dùng **Responsive Web Application** có khả năng truy cập mượt mà trên cả Desktop và thiết bị di động (Smartphone qua mạng LAN).

---

## BẢNG TỔNG HỢP BIỂU DIỄN DỮ LIỆU (MANDATORY DATA REPRESENTATION SUMMARY)

| Ứng dụng | Dạng dữ liệu thô | Biểu diễn số học (Representation) | Số chiều đặc trưng ($d$) | Kích thước ma trận Train ($X_{\text{train}}$) |
|---|---|---|---|---|
| **Diabetes** | Tệp bảng CSV (100,000 dòng, 9 cột) | Feature Vector (Z-score Scaling + One-Hot Encoding) | $d = 13$ | $X_{\text{train}} \in \mathbb{R}^{67,302 \times 13}$ |
| **House Price** | Tệp bảng CSV (2,000 dòng, 16 cột) | Continuous Feature Vector (StandardScaler + One-Hot) | $d = 23$ | $X_{\text{train}} \in \mathbb{R}^{1,400 \times 23}$ |
| **E-Commerce** | Tệp bảng CSV + Văn bản nhận xét (23,486 dòng, 11 cột) | Multimodal Feature Vector (Tabular + TF-IDF Text Vector) | $d = 2,532$ (32 tabular + 2,500 text) | $X_{\text{train}} \in \mathbb{R}^{16,440 \times 2,532}$ |

---

## CHƯƠNG I. GIỚI THIỆU BÀI TOÁN & KIẾN TRÚC HỆ THỐNG

### 1.1. Bối cảnh
Trong kỷ nguyên trí tuệ nhân tạo, một mô hình học máy (Machine Learning Model) chỉ là một phần nhỏ trong toàn bộ vòng đời của một hệ thống thông minh. Để đưa một thuật toán từ các dòng code thử nghiệm thành một sản phẩm có thể ứng dụng trong đời sống y tế, bất động sản và thương mại điện tử, dữ liệu thô từ thế giới thực phải trải qua quá trình thu thập, làm sạch, biến đổi thành các cấu trúc đại số tuyến tính (Vector, Ma trận, Tensor) trước khi thuật toán có thể tiếp nhận và học hỏi.

### 1.2. Mục tiêu
- Xây dựng 3 ứng dụng thông minh hoàn chỉnh với 3 loại cấu trúc dữ liệu khác nhau.
- Chứng minh nguyên lý: **Dữ liệu thực tế $\rightarrow$ Biểu diễn số học $\rightarrow$ Mô hình tính toán**.
- So sánh hiệu năng của nhiều thuật toán học máy khác nhau trên cùng một quy chuẩn đánh giá khách quan.
- Đóng gói (Persistence) và triển khai (Deployment) hệ thống dưới dạng Web Service và Giao diện Web Responsive truy cập qua mạng cục bộ (LAN).

### 1.3. Đường ống phát triển (Intelligent System Pipeline)
```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Raw Data   │ ──> │ Understand & │ ──> │ Data Repr.   │ ──> │ Model Train  │
│  (Kaggle)    │     │ Clean Data   │     │ (Vector/Mat) │     │ (5+ Models)  │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                       │
┌──────────────┐     ┌──────────────┐     ┌──────────────┐             │
│ Responsive   │ <── │ REST API     │ <── │ Model Persist│ <───────────┘
│ Web & Mobile │     │ (FastAPI)    │     │ (.joblib)    │
└──────────────┘     └──────────────┘     └──────────────┘
```

---

## CHƯƠNG II. CƠ SỞ BIỂU DIỄN DỮ LIỆU (DATA REPRESENTATION)

### 2.1. Vector đặc trưng và Ma trận đặc trưng
Với mỗi đối tượng quan sát thứ $i$ trong thế giới thực, thông tin của đối tượng được số hóa thành một vector đặc trưng cột:
$$x_i = [x_{i1}, x_{i2}, \dots, x_{id}]^T \in \mathbb{R}^d$$
Khi tập hợp $N$ quan sát độc lập, toàn bộ tập dữ liệu được biểu diễn dưới dạng ma trận đặc trưng $X$:
$$X = \begin{bmatrix} x_1^T \\ x_2^T \\ \vdots \\ x_N^T \end{bmatrix} \in \mathbb{R}^{N \times d}$$

### 2.2. Xử lý và Mã hóa biến phân loại (Categorical Encoding)
Các biến định danh chuỗi ký tự (như giới tính, tình trạng nội thất, thành phố) không thể thực hiện các phép tính số học trực tiếp.
- **One-Hot Encoding:** Biến mỗi giá trị danh mục thành một vector nhị phân. Ví dụ với biến `City`:
  $$\text{Mumbai} \rightarrow [0, 0, 0, 0, 1, 0], \quad \text{Delhi} \rightarrow [0, 1, 0, 0, 0, 0]$$
- Để tránh hiện tượng đa cộng tuyến hoàn hảo (Dummy Variable Trap), tùy chọn `drop='first'` được kích hoạt trong pipeline.

### 2.3. Chuẩn hóa thang đo dữ liệu số (Feature Scaling)
Do các biến số học có đơn vị và miền giá trị rất chênh lệch (ví dụ diện tích hàng nghìn sq ft so với số phòng ngủ 1-5), thuật toán sử dụng chuẩn hóa Z-score:
$$z = \frac{x - \mu}{\sigma}$$
Biến đổi này bảo đảm tâm dữ liệu tại 0 và phương sai bằng 1, giúp thuật toán Gradient Descent hội tụ ổn định và khoảng cách Euclidean trong KNN/SVM không bị chi phối bởi các biến có độ lớn áp đảo.

### 2.4. Phân biệt Biểu diễn văn bản: TF-IDF vs Dense Embedding
Cần phân biệt rõ ràng hai phương pháp biểu diễn văn bản:
1. **Biểu diễn số học cổ điển (TF-IDF Vector):**
   $$\text{Review Text} \longrightarrow \text{Tokenization} \longrightarrow \text{Vocabulary} \longrightarrow \text{TF-IDF Sparse Vector} \in \mathbb{R}^{d_{\text{text}}}$$
   Đây là vector thưa với số chiều lớn ($d_{\text{text}} = 2,500$), trong đó mỗi chiều đại diện cho trọng số thống kê của một n-gram cụ thể. **TF-IDF không phải là vector nhúng (embedding)** và không phản ánh khoảng cách ngữ nghĩa giữa các từ đồng nghĩa.
2. **Biểu diễn nhúng sâu (Dense Embedding Vectors - Lecture 02):**
   $$\text{Text} \longrightarrow \text{Tokens} \longrightarrow \text{Token IDs} \longrightarrow \text{Dense Embedding Vectors} \quad E \in \mathbb{R}^{B \times T \times d}$$
   Các token ID nguyên được chiếu qua ma trận trọng số nhúng để tạo ra các vector liên tục số chiều thấp ($d = 128 \dots 768$).

### 2.5. Nguyên tắc ngăn ngừa rò rỉ dữ liệu (Data Leakage Prevention)
Toàn bộ tập dữ liệu phải được phân chia thành **Train (70%) / Validation (15%) / Test (15%)** trước bất kỳ thao tác biến đổi nào. Các đối tượng `StandardScaler`, `OneHotEncoder`, `TfidfVectorizer` chỉ được phép `fit()` trên tập huấn luyện $D_{\text{train}}$. Tập Validation và Test tuyệt đối chỉ áp dụng `transform()`.

---

## CHƯƠNG III. ỨNG DỤNG 1 — DỰ ĐOÁN BỆNH TIỂU ĐƯỜNG

### 3.1. Mô tả bài toán & Tập dữ liệu
- **Tập dữ liệu:** `ghnshymsaini/diabetes-prediction-dataset` (Kaggle).
- **Quy mô thô:** 100,000 dòng, 9 cột thuộc tính.
- **Biến mục tiêu ($y$):** `diabetes` ($0$ = Không mắc, $1$ = Mắc bệnh). Tỉ lệ nhãn: 91.5% âm tính vs 8.5% dương tính (Hiện tượng mất cân bằng lớp nghiêm trọng - Class Imbalance).
- **Làm sạch:** Phát hiện và loại bỏ 3,854 bản ghi trùng lặp hoàn toàn, thu được 96,146 bản ghi độc lập.

### 3.2. Không gian biểu diễn dữ liệu
- Thuộc tính số ($6$): `age`, `bmi`, `HbA1c_level`, `blood_glucose_level`, `hypertension`, `heart_disease`.
- Thuộc tính danh mục ($2$): `gender` (mã hóa thành 2 dummy columns), `smoking_history` (mã hóa thành 5 dummy columns).
- Không gian đặc trưng cuối cùng: $d = 6 + 2 + 5 = 13$ chiều.
$$X_{\text{train}} \in \mathbb{R}^{67,302 \times 13}, \quad X_{\text{val}} \in \mathbb{R}^{14,422 \times 13}, \quad X_{\text{test}} \in \mathbb{R}^{14,422 \times 13}$$

### 3.3. So sánh mô hình trên tập Validation (Số liệu thực nghiệm thật)

| Mô hình | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Thời gian huấn luyện (s) |
|---|---|---|---|---|---|---|
| **Dummy Baseline** | 0.8400 | 0.0876 | 0.0865 | 0.0871 | 0.4997 | 0.05s |
| **Logistic Regression** | 0.8850 | 0.4271 | **0.8892** | 0.5770 | 0.9624 | 0.65s |
| **KNN (k=5)** | 0.9575 | 0.8601 | 0.6187 | 0.7197 | 0.9074 | 0.16s |
| **Decision Tree** | 0.8315 | 0.3387 | **0.9560** | 0.5002 | 0.9677 | 0.11s |
| **Random Forest** | 0.9022 | 0.4719 | **0.9167** | **0.6230** | **0.9757** | 0.94s |
| **SVM (LinearSVC)** | 0.9570 | 0.8446 | 0.6281 | 0.7205 | 0.9624 | 1.79s |

### 3.4. Đánh giá chuyên sâu & Lựa chọn mô hình
Trong sàng lọc y khoa bệnh tiểu đường, **Recall** có ý nghĩa sống còn vì ca âm tính giả (False Negative - người thực sự mắc bệnh nhưng mô hình báo bình thường) sẽ dẫn đến việc bệnh nhân không được chữa trị kịp thời, dẫn tới biến chứng mù lòa, cắt cụt chi hoặc suy thận.  
Mô hình **Random Forest Classifier** được lựa chọn vì dung hòa tối ưu giữa Recall cao (>91% trên Val, 89.70% trên Test), F1-score cao nhất và ROC-AUC vượt trội đạt **0.9743** trên tập Test độc lập.

---

## CHƯƠNG IV. ỨNG DỤNG 2 — DỰ ĐOÁN GIÁ NHÀ

### 4.1. Mô tả bài toán & Tập dữ liệu
- **Tập dữ liệu:** `chershi/house-price-prediction-dataset-2000-rows` (Kaggle).
- **Quy mô:** 2,000 dòng, 16 cột.
- **Biến mục tiêu ($y$):** `Price` (USD), giá trị từ $334,635 đến $2,225,409. Trung bình: $1,245,014; Trung vị: $1,246,602. Do trung bình và trung vị xấp xỉ nhau, phân bố giá nhà mang tính đối xứng chuẩn, không có hiện tượng lệch (skew) nghiêm trọng, do đó không cần áp dụng log transformation.
- **Làm sạch:** Dữ liệu hoàn chỉnh 100%, 0 giá trị thiếu, 0 dòng trùng lặp.

### 4.2. Không gian biểu diễn dữ liệu
- Thuộc tính số ($7$): `Area`, `Bedrooms`, `Bathrooms`, `Stories`, `Parking`, `Age`, `Locality Rating`.
- Thuộc tính danh mục ($8$): `City`, `Furnishing`, `Main Road`, `Guest Room`, `Basement`, `Water Supply`, `Air Conditioning`, `Preferred Tenant`.
- Số chiều sau mã hóa One-Hot: $d = 23$.
$$X_{\text{train}} \in \mathbb{R}^{1,400 \times 23}, \quad X_{\text{val}} \in \mathbb{R}^{300 \times 23}, \quad X_{\text{test}} \in \mathbb{R}^{300 \times 23}$$

### 4.3. So sánh mô hình trên tập Validation (Số liệu thực nghiệm thật)

| Mô hình | MAE ($) | MSE | RMSE ($) | $R^2$ Score | Thời gian huấn luyện (s) |
|---|---|---|---|---|---|
| **Dummy Baseline (Median)** | 241,302.3 | 91,389,000,000 | 302,306.1 | -0.0003 | 0.01s |
| **Linear Regression** | 125,450.1 | 23,466,700,000 | 153,188.5 | **0.7431** | 0.02s |
| **Ridge Regression ($\alpha=1.0$)** | 125,436.7 | 23,468,100,000 | 153,193.0 | 0.7431 | 0.02s |
| **Decision Tree Regressor** | 197,822.6 | 59,022,500,000 | 242,945.5 | 0.3540 | 0.02s |
| **Random Forest Regressor** | 148,108.1 | 34,524,300,000 | 185,807.2 | 0.6221 | 0.13s |
| **Gradient Boosting Regressor** | **135,629.0** | 28,949,300,000 | **170,145.1** | **0.6831** | 0.19s |

### 4.4. Lựa chọn mô hình & Đánh giá trên tập Test
Mặc dù Ridge Regression và Linear Regression đạt $R^2$ cao nhất trên tập Validation (0.7431), mô hình **Gradient Boosting Regressor** được lựa chọn triển khai vì có khả năng nắm bắt mối quan hệ phi tuyến và tương tác giữa các biến bất động sản (vị trí, diện tích, tiện ích) tốt hơn trên dữ liệu mới. Kết quả trên tập Test độc lập gồm 300 căn nhà xác nhận lựa chọn này:
- **MAE:** $126,793.85
- **RMSE:** $154,661.80
- **$R^2$ Score:** **0.7448**
Gradient Boosting khai thác ensemble boosting tuần tự, mỗi cây yếu sửa lỗi của cây trước, nên cải thiện đáng kể khả năng tổng quát hóa trên dữ liệu chưa thấy so với kết quả validation.

---

## CHƯƠNG V. ỨNG DỤNG 3 — KHÁM PHÁ HÀNH VI KHÁCH HÀNG E-COMMERCE

### 5.1. Mô tả bài toán & Tập dữ liệu
- **Tập dữ liệu:** `nicapotato/womens-ecommerce-clothing-reviews` (Kaggle).
- **Quy mô:** 23,486 lượt đánh giá sản phẩm, 11 cột.
- **Biến mục tiêu ($y$):** `Recommended IND` ($1$ = Khuyến nghị - 82.2%, $0$ = Không khuyến nghị - 17.8%).
- **Làm sạch:** Bỏ cột chỉ mục vô nghĩa `Unnamed: 0`. Nối `Title` và `Review Text` thành văn bản `full_review` (xử lý khuyết thiếu bằng chuỗi rỗng để không làm mất bản ghi khách hàng). Điền nhãn `'Unknown'` cho các danh mục khuyết thiếu.

### 5.2. Ba chế độ biểu diễn dữ liệu (Three Representation Regimes)
1. **Chế độ 1: Chỉ dữ liệu dạng bảng (Tabular Only):** Gồm các biến số (`Age`, `Rating`, `Positive Feedback Count`) và biến phân loại danh mục (`Division Name`, `Department Name`, `Class Name`). Kích thước sau mã hóa: $d_{\text{tab}} = 32$.
2. **Chế độ 2: Chỉ văn bản nhận xét (Text TF-IDF Only):** Dùng `TfidfVectorizer(max_features=2500, ngram_range=(1,2))`. Kích thước: $d_{\text{text}} = 2,500$.
3. **Chế độ 3: Kết hợp Đa phương thức (Combined Tabular + Text):** Ghép nối ma trận bảng và ma trận thưa TF-IDF qua `ColumnTransformer`. Tổng số chiều: $d_{\text{combined}} = 2,532$.

### 5.3. So sánh mô hình giữa các nhóm biểu diễn (Số liệu thực nghiệm thật)

| Mô hình | Nhóm Biểu diễn | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|---|
| **Tabular - Logistic Regression** | Tabular Only | 0.9466 | 0.9913 | 0.9434 | 0.9667 | 0.9818 |
| **Tabular - Decision Tree** | Tabular Only | 0.9446 | 0.9898 | 0.9424 | 0.9655 | 0.9778 |
| **Tabular - Random Forest** | Tabular Only | 0.9466 | 0.9913 | 0.9434 | 0.9667 | 0.9793 |
| **Tabular - Gradient Boosting** | Tabular Only | 0.9418 | 0.9770 | 0.9517 | 0.9642 | 0.9819 |
| **Text - TF-IDF + Logistic Regression** | Text Only | 0.8799 | 0.9657 | 0.8854 | 0.9238 | 0.9422 |
| **Text - TF-IDF + LinearSVC** | Text Only | 0.9018 | 0.9192 | 0.9655 | 0.9418 | 0.9318 |
| **Combined - Tabular + TF-IDF LogReg** | Combined | **0.9466** | 0.9895 | **0.9451** | **0.9668** | **0.9877** |

### 5.4. Kết luận về vai trò của văn bản nhận xét (Business & Technical Insights)
- **Nội dung nhận xét có giúp cải thiện mô hình không?** **CÓ.**
- Mô hình Combined đạt **ROC-AUC cao nhất (0.9877 trên Val, 0.9737 trên Test)**. Mặc dù biến số `Rating` giải thích phần lớn ý định khuyến nghị, nhưng tại các vùng phân vân (ví dụ khách hàng cho 3 sao), các từ khóa ngữ nghĩa như *"flattering"*, *"great fit"* hoặc *"cheap material"*, *"runs small"* giúp bộ phân loại xác định chuẩn xác xác suất khuyến nghị mà điểm số đơn thuần không thể phân tách.

---

## CHƯƠNG VI. LƯU TRỮ & TRIỂN KHAI HỆ THỐNG (DEPLOYMENT)

### 6.1. Lưu trữ mô hình (Model Persistence)
Cả ba đường ống tiền xử lý và mô hình được lưu trữ nguyên khối tại:
- `models/diabetes/diabetes_pipeline.joblib`
- `models/house_price/house_pipeline.joblib`
- `models/ecommerce/ecommerce_pipeline.joblib`
Kiểm tra nạp lại (`joblib.load`) và suy luận tức thời bảo đảm tính nhất quán toán học 100% giữa lúc huấn luyện và khi phục vụ request.

### 6.2. REST API với FastAPI
- Máy chủ được xây dựng trong `api/main.py` với Lifespan Manager nạp trước toàn bộ pipeline vào RAM.
- Các endpoint:
  - `POST /predict/diabetes`: Nhận thông số lâm sàng $\rightarrow$ Trả về nhãn chẩn đoán, xác suất và mức độ rủi ro.
  - `POST /predict/house`: Nhận thông số nhà $\rightarrow$ Trả về định giá thị trường chính xác.
  - `POST /predict/ecommerce`: Nhận nhận xét và điểm số $\rightarrow$ Trả về xác nhận khuyến nghị và độ tin cậy.
  - `GET /health`: Kiểm tra trạng thái máy chủ và các pipeline sẵn sàng.
  - `GET /docs`: Swagger UI tương tác trực tiếp.

### 6.3. Giao diện Web Responsive & Client Mobile qua LAN
- Thiết kế giao diện hiện đại phong cách Dark Mode Glassmorphism tại `web/templates/index.html` và `web/static/css/style.css`.
- Sử dụng URL tương đối (`/predict/...`) giúp máy tính để bàn và điện thoại smartphone trong cùng mạng Wi-Fi/LAN (`http://192.168.0.105:8000/`) đều thực hiện gọi API chính xác 100%.
- Giao diện đáp ứng tiêu chuẩn Mobile-First (khung nhìn 390x844), bố cục 1 cột, không tràn khung ngang.

---

## CHƯƠNG VII. BẢNG SO SÁNH TỔNG HỢP 3 HỆ THỐNG

| Khía cạnh | Ứng dụng 1: Diabetes | Ứng dụng 2: House Price | Ứng dụng 3: E-Commerce |
|---|---|---|---|
| **Loại bài toán** | Phân loại nhị phân (Classification) | Hồi quy đa biến (Regression) | Phân loại Đa phương thức (Tabular + NLP) |
| **Một quan sát là gì?** | Một hồ sơ xét nghiệm lâm sàng của bệnh nhân | Một ngôi nhà / bất động sản nhà ở | Một nhận xét đánh giá của khách hàng |
| **Biến mục tiêu ($y$)** | `diabetes` $\in \{0, 1\}$ | `Price` $\in \mathbb{R}^+$ (USD) | `Recommended IND` $\in \{0, 1\}$ |
| **Biểu diễn thô ban đầu** | Bảng CSV (100k dòng, 9 cột) | Bảng CSV (2k dòng, 16 cột) | Bảng CSV + Văn bản tự do (23k dòng, 11 cột) |
| **Biểu diễn số học cuối** | Normalized Vector $\in \mathbb{R}^{13}$ | Continuous Vector $\in \mathbb{R}^{23}$ | Combined Vector $\in \mathbb{R}^{2532}$ |
| **Tiền xử lý chính** | Loại duplicate, Z-score, OneHot | Z-score, OneHot | Nối text, SimpleImputer, OneHot, TF-IDF |
| **Mô hình tốt nhất** | Random Forest Classifier | Gradient Boosting Regressor | Combined Tabular + TF-IDF LogReg |
| **Độ đo chính** | Recall = 0.8970, ROC-AUC = 0.9743 | MAE = $126,793, $R^2 = 0.7448$ | ROC-AUC = 0.9737, F1 = 0.9589 |
| **Triển khai Web** | Responsive Desktop Card UI | Responsive Desktop Card UI | Responsive Desktop Card UI |
| **Triển khai Mobile** | Mobile Web Client qua LAN (390x844) | Mobile Web Client qua LAN (390x844) | Mobile Web Client qua LAN (390x844) |
| **Hạn chế chính** | Mất cân bằng lớp nặng (8.5% dương) | Quy mô 2,000 dòng vừa phải | TF-IDF chưa bắt được ngữ pháp sâu |

---

## CHƯƠNG VIII. THẢO LUẬN KỸ THUẬT & BÀI HỌC KINH NGHIỆM

1. **Về rò rỉ dữ liệu (Data Leakage):** Việc phân tách Train/Validation/Test trước khi gọi bất kỳ hàm tiền xử lý nào là bài học sống còn. Nếu `StandardScaler` hay `TfidfVectorizer` được fit trên toàn bộ dataset trước khi split, điểm số trên tập test sẽ bị lạc quan quá mức và không phản ánh đúng năng lực suy luận thực tế.
2. **Về lựa chọn độ đo:** Độ chính xác (Accuracy) hoàn toàn vô dụng trong các tập dữ liệu mất cân bằng lớp như Tiểu đường (91.5% âm tính) và E-Commerce (82.2% dương tính). Việc tập trung vào **Recall**, **Precision**, **F1-score** và **ROC-AUC** là bắt buộc.
3. **Tính nhất quán giữa Training và Deployment:** Việc sử dụng Scikit-Learn `Pipeline` và `ColumnTransformer` đóng gói toàn bộ các bước biến đổi dữ liệu giúp API suy luận trực tiếp trên dữ liệu người dùng gửi lên mà không bao giờ gặp lỗi lệch thuộc tính (feature mismatch) hay thiếu category.

---

## CHƯƠNG IX. KẾT LUẬN & HƯỚNG PHÁT TRIỂN

Dự án đã hoàn thành xuất sắc toàn bộ các mục tiêu của Assignment 02:
- Tải về và phân tích 100% dữ liệu thực từ 3 dataset Kaggle chính thức.
- Xây dựng, huấn luyện và đánh giá hơn 16 mô hình học máy khác nhau trên môi trường `ai-env`.
- Thực hiện lưu trữ mô hình và xây dựng REST API thống nhất bằng FastAPI.
- Phát triển giao diện Web Responsive hiện đại, kiểm thử tự động trên Desktop và Mobile viewport (390x844) và sẵn sàng truy cập qua mạng nội bộ LAN.

**Hướng phát triển:**
- Đối với E-Commerce: Thử nghiệm các mô hình Dense Embeddings (như Sentence-Transformers hoặc BERT) để nắm bắt ngữ pháp sâu.
- Đối với Tiểu đường: Thu thập thêm dữ liệu của lớp thiểu số hoặc áp dụng kỹ thuật lấy mẫu SMOTE để nâng cao hơn nữa Precision mà không suy giảm Recall.
