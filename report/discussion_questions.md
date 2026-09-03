# DISCUSSION QUESTIONS & AUTHENTIC TECHNICAL ANSWERS
**Môn học:** Phát triển các hệ thống thông minh / Intelligent System Development (Assignment 02)
**Học viện Công nghệ Bưu chính Viễn thông (PTIT)**
**Môi trường thực nghiệm:** `ai-env` (Python 3.12.13, Scikit-Learn 1.4+, FastAPI 0.110+)

Tất cả các câu trả lời dưới đây đều dựa trên **kết quả thực nghiệm thực tế** sau khi chạy trên 3 tập dữ liệu Kaggle chính thức.

---

## PHẦN 1: 15 CÂU HỎI THẢO LUẬN CHUNG CHO 3 ỨNG DỤNG

### Câu 1: Một quan sát (observation) đại diện cho đối tượng gì?
- **Ứng dụng 1 (Diabetes):** Một quan sát đại diện cho **hồ sơ bệnh án của một bệnh nhân lâm sàng**, chứa các thông tin nhân khẩu học (giới tính, tuổi) và các chỉ số xét nghiệm sinh lý/hóa sinh (BMI, đường huyết, HbA1c, tiền sử bệnh tim, cao huyết áp).
- **Ứng dụng 2 (House Price):** Một quan sát đại diện cho **một căn nhà/bất động sản nhà ở** được chào bán, với các thông số vật lý (diện tích, số phòng ngủ, số phòng tắm, tầng, chỗ đỗ xe) và các thuộc tính vị trí, tiện nghi (thành phố, nội thất, điều hòa, đường chính).
- **Ứng dụng 3 (E-Commerce):** Một quan sát đại diện cho **một lượt đánh giá sản phẩm của một khách hàng nữ**, gồm thông tin nhân khẩu (tuổi), phản hồi số học (số sao rating, số lượt thích) và nhận xét ngôn ngữ tự nhiên (tiêu đề và nội dung review).

---

### Câu 2: Biểu diễn dữ liệu thô ban đầu (Raw Representation) là gì?
- **Ứng dụng 1:** Tệp bảng CSV `diabetes_prediction_dataset.csv`, $N = 100,000$ dòng, 9 cột; chứa dữ liệu hỗn hợp: chuỗi ký tự (`gender`, `smoking_history`), số nguyên (`hypertension`, `heart_disease`, `blood_glucose_level`, `diabetes`) và số thực (`age`, `bmi`, `HbA1c_level`).
- **Ứng dụng 2:** Tệp bảng CSV `enhanced_house_price_dataset.csv`, $N = 2,000$ dòng, 16 cột; chứa số nguyên (`Area`, `Bedrooms`, `Bathrooms`, `Stories`, `Parking`, `Age`, `Locality Rating`, `Price`) và chuỗi phân loại (`City`, `Furnishing`, `Main Road`, v.v.).
- **Ứng dụng 3:** Tệp bảng CSV kết hợp văn bản tự do `Womens Clothing E-Commerce Reviews.csv`, $N = 23,486$ dòng, 11 cột; chứa các chuỗi văn bản nhận xét tự do (`Title`, `Review Text`) kết hợp với dữ liệu số và danh mục.

---

### Câu 3: Biểu diễn số học cuối cùng (Final Numerical Representation) đưa vào mô hình là gì?
- **Ứng dụng 1:** Vector đặc trưng chuẩn hóa trong không gian thực:
  $$x_i \in \mathbb{R}^{13}$$
  Toàn bộ tập dữ liệu huấn luyện là ma trận đặc trưng thưa/đặc:
  $$X_{\text{train}} \in \mathbb{R}^{67,302 \times 13}, \quad y_{\text{train}} \in \{0, 1\}^{67,302}$$
- **Ứng dụng 2:** Vector đặc trưng liên tục:
  $$x_i \in \mathbb{R}^{23}, \quad y_i \in \mathbb{R}$$
  Ma trận huấn luyện:
  $$X_{\text{train}} \in \mathbb{R}^{1,400 \times 23}, \quad y_{\text{train}} \in \mathbb{R}^{1,400}$$
- **Ứng dụng 3 (Combined):** Vector đặc trưng kết hợp (Multimodal Representation) bao gồm 32 chiều đặc trưng bảng và 2,500 chiều vector thưa TF-IDF:
  $$x_i \in \mathbb{R}^{2,532}, \quad X_{\text{train}} \in \mathbb{R}^{16,440 \times 2,532}, \quad y_{\text{train}} \in \{0, 1\}^{16,440}$$

---

### Câu 4: Ý nghĩa các chiều của ma trận đặc trưng (Shape dimensions) là gì?
- Đối với ma trận $X \in \mathbb{R}^{N \times d}$:
  - **Chiều thứ nhất ($N$):** Đại diện cho số lượng mẫu/quan sát độc lập (số bệnh nhân, số ngôi nhà, số lượt đánh giá).
  - **Chiều thứ hai ($d$):** Đại diện cho số chiều của không gian đặc trưng sau khi đã qua tiền xử lý, chuẩn hóa và mã hóa.
  - Ví dụ trong Tiểu đường: $d=13$ gồm 6 đặc trưng số học (Age, BMI, HbA1c, Blood Glucose, Hypertension, Heart Disease) + 2 biến dummy giới tính + 5 biến dummy tiền sử hút thuốc.

---

### Câu 5: Những đặc trưng nào bắt buộc phải mã hóa (Encoding)?
- **Ứng dụng 1:** Cột `gender` (3 nhóm) và `smoking_history` (6 nhóm). Áp dụng One-Hot Encoding với tùy chọn `drop='first'` để triệt tiêu hiện tượng đa cộng tuyến hoàn hảo (multicollinearity).
- **Ứng dụng 2:** 8 cột phân loại: `City` (7 thành phố), `Furnishing` (3 mức), `Main Road`, `Guest Room`, `Basement`, `Water Supply`, `Air Conditioning`, `Preferred Tenant`. Áp dụng One-Hot Encoding.
- **Ứng dụng 3:** Các danh mục sản phẩm: `Division Name`, `Department Name`, `Class Name`. Sử dụng One-Hot Encoding kết hợp SimpleImputer (`fill_value='Unknown'`).

---

### Câu 6: Những đặc trưng nào cần chuẩn hóa (Normalization / Scaling)?
- Tất cả các đặc trưng số học liên tục có thang đo chênh lệch lớn:
  - **Tiểu đường:** `age` (0.08 - 80), `bmi` (10 - 60), `blood_glucose_level` (80 - 300), `HbA1c_level` (3.5 - 9.0). Sử dụng `StandardScaler` ($z = \frac{x - \mu}{\sigma}$). Việc chuẩn hóa là bắt buộc đối với Logistic Regression, KNN và SVM để hàm khoảng cách Euclidean và gradient descent hội tụ chính xác.
  - **Giá nhà:** `Area` (lên đến 15,000 sq ft) so với `Bedrooms` (1-5) và `Age` (0-80). Sử dụng `StandardScaler` giúp các mô hình tuyến tính và Gradient Boosting xử lý công bằng các đặc trưng có thang đo khác nhau.
  - **E-Commerce:** `Age`, `Rating`, `Positive Feedback Count`.

---

### Câu 7: Thông tin nào bị mất mát (lost) trong quá trình biểu diễn dữ liệu?
1. **Trong dữ liệu văn bản (E-Commerce):** Khi sử dụng túi từ TF-IDF (Bag-of-Words n-gram), toàn bộ **cấu trúc ngữ pháp, thứ tự từ dài (long-range word order), sắc thái ngữ điệu, ngữ cảnh phức tạp** bị mất mát. Mô hình chỉ biết các cụm 1-2 từ có mặt với trọng số bao nhiêu, không hiểu cấu trúc cú pháp phân cấp.
2. **Trong dữ liệu số:** Chuẩn hóa Z-score làm mất giá trị đơn vị đo vật lý thực tế (ví dụ mg/dL đường huyết hay sq ft diện tích), biến tất cả thành độ lệch chuẩn quanh giá trị 0.
3. **Khi loại bỏ dòng trùng lặp:** 3,854 dòng trùng lặp trong bộ dữ liệu Tiểu đường bị lược bỏ để bảo đảm tính phân tách độc lập giữa các tập, làm giảm nhẹ mật độ phân bố tự nhiên của các ca bệnh điển hình.

---

### Câu 8: Thông tin nào được bảo toàn (preserved) trong quá trình biểu diễn?
1. **Phân bố thống kê tương đối:** Tỉ lệ tương quan, phương sai và xếp hạng tương đối giữa các quan sát được bảo toàn nguyên vẹn qua phép biến đổi afin chuẩn hóa.
2. **Mối quan hệ nhân quả/tương quan:** Tương quan mạnh giữa HbA1c và nồng độ đường huyết đối với khả năng mắc bệnh tiểu đường được giữ nguyên.
3. **Từ khóa cảm xúc then chốt:** Các từ mang cực tính cảm xúc cao trong nhận xét khách hàng (e.g., *"love"*, *"perfect"*, *"flattering"*, *"cheap"*, *"terrible"*, *"disappointed"*) nhận trọng số TF-IDF cao, giúp bộ phân loại xác định chính xác ý định khuyến nghị.

---

### Câu 9: Những bước tiền xử lý nào có nguy cơ gây rò rỉ dữ liệu (Data Leakage)?
- **Nguy cơ lớn nhất:** Áp dụng `fit()` hoặc `fit_transform()` của `StandardScaler`, `SimpleImputer`, `OneHotEncoder`, hoặc `TfidfVectorizer` trên **toàn bộ tập dữ liệu $D$ trước khi chia tách** Train / Test.
- **Hậu quả:** Giá trị trung bình $\mu_{\text{all}}$ và phương sai $\sigma_{\text{all}}$ (hoặc từ điển từ vựng của tập test) bị rò rỉ vào không gian huấn luyện, khiến mô hình đạt điểm số cao ảo trên tập kiểm thử nhưng suy giảm mạnh khi đối mặt với dữ liệu thực tế.
- **Giải pháp trong project:** **Chia tập trước (Split First)**; toàn bộ các bộ biến đổi chỉ được `fit()` duy nhất trên tập Train, tập Validation và Test chỉ được gọi `transform()`.

---

### Câu 10: Mô hình nào đạt hiệu năng tốt nhất cho từng ứng dụng?
- **Ứng dụng 1 (Diabetes):** **Random Forest Classifier** đạt cân bằng xuất sắc nhất (Recall trên Test = 89.70%, ROC-AUC = 0.9743, F1 = 0.6082).
- **Ứng dụng 2 (House Price):** **Gradient Boosting Regressor** đạt $R^2 = 0.7448$ trên Test với MAE = $126,793. Mặc dù Ridge Regression có $R^2$ Validation cao nhất (0.7431), Gradient Boosting tổng quát hóa tốt hơn trên dữ liệu mới.
- **Ứng dụng 3 (E-Commerce):** **Combined Tabular + TF-IDF Logistic Regression** đạt ROC-AUC cao nhất (0.9877 trên Val, 0.9737 trên Test, Accuracy = 93.41%).

---

### Câu 11: Tại sao lại lựa chọn mô hình đó?
- **Diabetes:** Trong bài toán chẩn đoán y khoa, giảm thiểu ca bệnh bị bỏ sót (False Negatives) là yếu tố sống còn. Random Forest với cấu trúc tập hợp cây quyết định và `class_weight='balanced'` học được các ranh giới phi tuyến tính phức tạp giữa tuổi, đường huyết và HbA1c, mang lại độ bao phủ chẩn đoán (Recall) gần 90%.
- **House Price:** Dữ liệu bất động sản có nhiều biến phân loại sau OneHot tạo ra 23 chiều, đồng thời mối quan hệ giữa giá nhà và các tiện nghi (vị trí, diện tích, hạ tầng) có tính phi tuyến. Gradient Boosting Regressor xây dựng ensemble tuần tự các cây quyết định yếu, mỗi cây sửa sai số dư của cây trước, cho phép nắm bắt tương tác đặc trưng phức tạp mà mô hình tuyến tính không thể hiện được. Kết quả Test ($R^2 = 0.7448$) xác nhận khả năng tổng quát hóa vượt trội.
- **E-Commerce:** Mô hình kết hợp dung hòa được tín hiệu định lượng mạnh (Rating sao) và tín hiệu ngữ nghĩa định tính (Review Text), giải quyết hoàn hảo các ca biên giới (như đánh giá 3 sao nhưng nhận xét khen ngợi hoặc phàn nàn).

---

### Câu 12: Độ đo đánh giá nào là quan trọng nhất cho từng ứng dụng?
- **Diabetes:** **Recall** (Sensitivity) và **ROC-AUC**. Một bệnh nhân tiểu đường bị dự đoán nhầm là bình thường (False Negative) sẽ không được can thiệp y tế, dẫn tới biến chứng mù lòa, suy thận hoặc đột quỵ. Ngược lại, dự đoán nhầm dương tính (False Positive) chỉ dẫn đến xét nghiệm máu khẳng định lại.
- **House Price:** **MAE** (Mean Absolute Error) và **$R^2$ Score**. MAE biểu thị trực tiếp bằng đơn vị tiền tệ USD ($) mà mô hình lệch trung bình so với giá thị trường, giúp nhà đầu tư dễ định giá.
- **E-Commerce:** **ROC-AUC** và **F1-Score**. Do lớp khuyến nghị chiếm ưu thế (82.2% lớp 1 vs 17.8% lớp 0), Accuracy bị đánh giá thiên lệch, do đó ROC-AUC và F1 phản ánh năng lực phân lớp thực chất.

---

### Câu 13: Mô hình được lưu trữ (Persist) như thế nào?
- Toàn bộ quy trình tiền xử lý (`ColumnTransformer`) và mô hình học máy (`Estimator`) được đóng gói nguyên khối vào đối tượng `sklearn.pipeline.Pipeline`.
- Sử dụng thư viện `joblib.dump(pipeline, filename)` để tuần tự hóa (serialize) thành tệp nhị phân `.joblib` tại:
  - `models/diabetes/diabetes_pipeline.joblib`
  - `models/house_price/house_pipeline.joblib`
  - `models/ecommerce/ecommerce_pipeline.joblib`
- Sau khi lưu, kiểm tra tính toàn vẹn bằng `joblib.load()` và chạy dự đoán trên mẫu mới ngay lập tức.

---

### Câu 14: Web Service sử dụng mô hình đã lưu trữ như thế nào?
- Tại thời điểm khởi động máy chủ FastAPI, cơ chế **Lifespan Context Manager** tự động gọi `joblib.load()` cho cả 3 tệp pipeline và lưu vào bộ nhớ RAM (`loaded_models` dictionary).
- Khi người dùng gửi request `POST /predict/...`, dữ liệu JSON được chuyển trực tiếp vào `pd.DataFrame` 1 dòng và đưa vào phương thức `pipeline.predict()` và `pipeline.predict_proba()`.
- Nhờ có Pipeline đóng gói, quá trình scale, encode và vectorize diễn ra tự động và bảo đảm tính nhất quán tuyệt đối giữa lúc huấn luyện và khi phục vụ người dùng.

---

### Câu 15: Ứng dụng Mobile giao tiếp với dịch vụ dự đoán như thế nào?
- Hệ thống sử dụng kiến trúc **Responsive Mobile Web Client**: Người dùng mở trình duyệt trên điện thoại và truy cập vào máy chủ thông qua mạng Wi-Fi nội bộ:
  ```text
  http://<LAN_IP>:8000/
  ```
- Khi người dùng bấm nút dự đoán, mã JavaScript trên điện thoại thực hiện lệnh gọi `fetch('/predict/...', { method: 'POST', body: JSON.stringify(...) })`.
- Do sử dụng URL tương đối (`/predict/...`), request tự động gửi về đúng IP của máy chủ host mà không gặp lỗi kết nối localhost. Kết quả JSON được parse và hiển thị mượt mà trên giao diện mobile.

---

## PHẦN 2: 6 CÂU HỎI BỔ SUNG CHO ỨNG DỤNG E-COMMERCE

### 1. Nội dung văn bản nhận xét (Customer Comments) chứa đựng những thông tin gì?
Nội dung nhận xét phản ánh những trải nghiệm thực tế mang tính chủ quan mà các chỉ số số học không thể hiện được:
- **Độ vừa vặn và kích cỡ:** Sản phẩm mặc lên rộng, chật, đúng size (*"runs small"*, *"true to size"*, *"flattering"*).
- **Chất liệu vải và độ bền:** Vải mềm, mỏng, ngứa, co giãn, chất liệu rẻ tiền (*"fabric is soft"*, *"itchy material"*, *"cheap polyester"*).
- **Tính thẩm mỹ và kiểu dáng:** Màu sắc thực tế so với hình ảnh (*"color looks faded"*, *"gorgeous dress"*).
- **Ý định hành vi:** Khách hàng dự định mặc đi dự tiệc, mặc đi làm, hoặc sẽ đem trả hàng (*"returned it immediately"*).

---

### 2. Văn bản nhận xét được chuyển đổi thành dữ liệu số như thế nào?
1. **Làm sạch văn bản:** Nối tiêu đề và nội dung, loại bỏ khoảng trắng thừa, xử lý giá trị khuyết thiếu.
2. **Tokenization:** Tách chuỗi ký tự thành các từ đơn (unigram) và cụm hai từ (bigram).
3. **Lọc Stop Words:** Loại bỏ các từ dừng tiếng Anh phổ biến (*"the"*, *"and"*, *"in"*).
4. **Tính toán TF-IDF:**
   $$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \log\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$$
5. **Vector hóa:** Mỗi văn bản trở thành một vector thưa $v \in \mathbb{R}^{2500}$ được chuẩn hóa chuẩn L2.

---

### 3. Token IDs trong bài giảng Lecture 02 đại diện cho điều gì?
- Trong xử lý ngôn ngữ tự nhiên hiện đại (Deep Learning / Transformers), **Token ID** là một số nguyên duy nhất ($i \in \{0, 1, \dots, |V|-1\}$) đại diện cho chỉ số của một từ hoặc một mảnh từ (subword token) trong từ điển từ vựng cố định (Vocabulary).
- Một câu văn bản sau khi qua Tokenizer sẽ trở thành một chuỗi các số nguyên:
  $$[\text{"I"}, \text{"love"}, \text{"this"}, \text{"dress"}] \longrightarrow [42, 1892, 48, 2031]$$
- Chuỗi Token ID này chưa mang ý nghĩa hình học mà chỉ đóng vai trò con trỏ chỉ mục để tra cứu vector trong bảng nhúng (Embedding Matrix).

---

### 4. Vector nhúng (Embedding Vectors) đại diện cho điều gì?
- **Embedding Vector** là một vector **đặc (dense)**, số chiều thấp hơn ($d \in [64, 768]$) biểu diễn vị trí của từ hoặc câu trong không gian ngữ nghĩa liên tục.
- Trong không gian nhúng, các từ có ngữ nghĩa tương đồng hoặc xuất hiện trong ngữ cảnh giống nhau sẽ có khoảng cách vector gần nhau (khoảng cách Cosine nhỏ).
- **Điểm khác biệt then chốt:** Vector TF-IDF là vector **thưa (sparse)** có số chiều bằng từ vựng ($2,500$ chiều) và không nắm bắt được ngữ nghĩa tương đồng giữa các từ đồng nghĩa (ví dụ *"gorgeous"* và *"beautiful"* là 2 chiều trực giao độc lập trong TF-IDF). Trong khi đó, Embedding Vector là vector **đặc (dense)** phản ánh hình học ngữ nghĩa sâu.

---

### 5. Những sở thích hoặc hành vi khách hàng nào có thể khám phá được từ dữ liệu?
1. **Mối liên hệ giữa Rating và Khuyến nghị:** Khách hàng đánh giá 4-5 sao gần như 100% sẽ khuyến nghị sản phẩm; đánh giá 1-2 sao hầu như không khuyến nghị. Tuy nhiên, nhóm đánh giá **3 sao** là nhóm ranh giới quan trọng, trong đó khách hàng thường cân nhắc giữa kiểu dáng đẹp nhưng chất liệu chưa ưng ý.
2. **Bộ phận sản phẩm được quan tâm nhiều nhất:** Bộ phận `Tops` và `Dresses` chiếm đa số lượng đánh giá (>70%), phản ánh đây là các mặt hàng mua sắm chủ lực của khách hàng nữ.
3. **Từ khóa biểu lộ sự hài lòng:** Các khách hàng có ý định khuyến nghị thường dùng từ khóa: *"love"*, *"perfect"*, *"great fit"*, *"flattering"*, *"comfortable"*.

---

### 6. Nội dung văn bản (Text) có thực sự cải thiện chất lượng mô hình so với chỉ dùng dữ liệu dạng bảng hay không?
- **Kết luận thực nghiệm:** **CÓ**.
- **Minh chứng số liệu thực tế trên tập dữ liệu:**
  - Mô hình chỉ dùng bảng (Tabular Gradient Boosting): Đạt ROC-AUC = **0.9819**.
  - Mô hình chỉ dùng văn bản (Text TF-IDF LogReg): Đạt ROC-AUC = **0.9422**.
  - Mô hình kết hợp cả Bảng và Văn bản (Combined Tabular + TF-IDF): Đạt ROC-AUC = **0.9877** trên Validation và **0.9737** trên Test.
- **Ý nghĩa kỹ thuật:** Việc bổ sung vector đặc trưng văn bản TF-IDF cung cấp thêm thông tin cực tính cảm xúc và ngữ cảnh sử dụng, giúp mô hình phân định chính xác các trường hợp "ranh giới" (điểm đánh giá trung bình 3 sao nhưng lời nhận xét khen ngợi hoặc chê bai rõ rệt).
