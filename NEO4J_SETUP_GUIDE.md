# Hướng dẫn Cài đặt Đồ thị Tri thức Neo4j

Tài liệu này hướng dẫn cách cài đặt và thiết lập phần mở rộng **Cơ sở dữ liệu Đồ thị Neo4j (Neo4j Graph Database)** cho bài toán Phân tích Hành vi Khách hàng Thương mại Điện tử trong dự án này.

Thay vì sử dụng các mô hình Học máy truyền thống (Logistic Regression, TF-IDF) vốn coi mỗi đánh giá của khách hàng là một sự kiện rời rạc và độc lập, việc tích hợp Neo4j cho phép chúng ta chuyển đổi dữ liệu dạng bảng (tabular data) thành một **Đồ thị Tri thức (Knowledge Graph)**. Đồ thị này sẽ liên kết chặt chẽ các thực thể: `Khách hàng (Customers)`, `Sản phẩm (Products)`, `Ngành hàng (Departments)`, và `Đánh giá (Reviews)` lại với nhau. Đây chính là nền tảng kiến trúc tiên tiến để xây dựng một Chatbot tư vấn mua sắm sử dụng công nghệ **Graph RAG (Retrieval-Augmented Generation)**.

---

## 1. Yêu cầu Cài đặt (Prerequisites)

Bạn có thể chạy Neo4j bằng Docker (Khuyên dùng) hoặc cài đặt Neo4j Desktop.

### Lựa chọn A: Sử dụng Docker (Khuyên dùng)
Chạy lệnh sau trên terminal để khởi tạo một container Neo4j phiên bản Enterprise có tích hợp sẵn plugin APOC (Awesome Procedures on Cypher):

```bash
docker run \
    -p 7474:7474 -p 7687:7687 \
    -d \
    --name neo4j-ecommerce \
    --env NEO4J_AUTH=neo4j/password \
    --env NEO4J_apoc_export_file_enabled=true \
    --env NEO4J_apoc_import_file_enabled=true \
    --env NEO4J_apoc_import_file_use__neo4j__config=true \
    --env NEO4J_PLUGINS='["apoc"]' \
    neo4j:5.12.0
```

### Lựa chọn B: Sử dụng Neo4j Desktop
1. Tải và cài đặt phần mềm [Neo4j Desktop](https://neo4j.com/download/).
2. Tạo một Database cục bộ (Local DBMS) và đặt mật khẩu là `password` (nếu đặt mật khẩu khác, bạn cần cập nhật lại trong file `scripts/neo4j_demo.py`).
3. Nhấn Start để chạy Database.

---

## 2. Nạp dữ liệu Thương mại điện tử vào Đồ thị

Khi Database của bạn đã chạy ở địa chỉ `bolt://localhost:7687` (hoặc `neo4j://localhost:7687`), bạn cần chạy kịch bản Cypher để tạo các điều kiện ràng buộc (constraints) và nạp dữ liệu mẫu vào đồ thị.

Dự án đã cung cấp sẵn một đoạn mã Python tự động kết nối với cơ sở dữ liệu Neo4j cục bộ của bạn. Mã nguồn này sẽ xóa sạch dữ liệu cũ (nếu có), thiết lập ràng buộc và đưa toàn bộ dữ liệu CSV đã làm sạch vào đồ thị.

Đảm bảo bạn đã kích hoạt đúng môi trường Python của dự án:
```bash
conda activate ai-env
pip install neo4j pandas
```

Chạy kịch bản tự động xây dựng đồ thị:
```bash
python scripts/neo4j_demo.py
```

---

## 3. Kiến trúc Lược đồ (Graph Schema)

Đoạn mã Cypher được thiết kế để tạo ra lược đồ (Schema) như sau:

### Các Nút (Nodes / Entities)
- `(:Customer {age: Integer})`: Đại diện cho người mua hàng để lại bình luận.
- `(:Product {class_name: String})`: Tên phân loại chi tiết của sản phẩm may mặc.
- `(:Department {name: String, division: String})`: Ngành hàng lớn mà sản phẩm thuộc về (ví dụ: Tops, Bottoms).
- `(:Review {text: String, rating: Integer, recommended: Boolean})`: Nội dung chi tiết của đánh giá và cảm xúc.

### Các Mối quan hệ (Relationships / Edges)
- `(Customer)-[:WROTE]->(Review)` : Khách hàng VIẾT Đánh giá.
- `(Review)-[:ABOUT]->(Product)` : Đánh giá nói VỀ Sản phẩm.
- `(Product)-[:BELONGS_TO]->(Department)` : Sản phẩm THUỘC VỀ Ngành hàng.

---

## 4. Truy vấn Đồ thị (Ví dụ mã Cypher)

Mở trình duyệt Neo4j Browser của bạn tại địa chỉ [http://localhost:7474](http://localhost:7474) (Tài khoản: `neo4j` / Mật khẩu: `password`). Bạn có thể thử chạy các truy vấn Cypher sau:

### Tìm Top 5 sản phẩm được khuyên dùng nhiều nhất thuộc Ngành hàng "Váy" (Dresses)
```cypher
MATCH (p:Product)-[:BELONGS_TO]->(d:Department {name: 'Dresses'})
MATCH (r:Review {recommended: true})-[:ABOUT]->(p)
RETURN p.class_name, count(r) AS PositiveReviews
ORDER BY PositiveReviews DESC
LIMIT 5;
```

### Lấy ngữ cảnh cho Graph RAG: Tìm tất cả các đánh giá của tập Khách hàng từ 25-30 tuổi cho sản phẩm "Áo kiểu" (Blouses)
```cypher
MATCH (c:Customer)-[:WROTE]->(r:Review)-[:ABOUT]->(p:Product {class_name: 'Blouses'})
WHERE c.age >= 25 AND c.age <= 30
RETURN c.age, r.rating, r.text
LIMIT 10;
```

---

## 5. Hướng phát triển tiếp theo: Tích hợp Chatbot Graph RAG

Khi cấu trúc đồ thị này đã đi vào hoạt động trơn tru, bước kiến trúc tiếp theo để hoàn thiện hệ thống là kết nối nó với một Mô hình Ngôn ngữ Lớn (LLM) như OpenAI GPT-4 hoặc LLaMA 3 cục bộ.

Khi một người dùng đặt câu hỏi: *"Các khách hàng nữ dưới 30 tuổi có cảm nhận thế nào về những chiếc váy mùa hè của cửa hàng?"*
1. **Trích xuất Thực thể (Entity Extraction)**: Mô hình LLM phân tách câu hỏi và xác định điều kiện `Product=Dresses` và `Customer.age < 30`.
2. **Truy xuất Đồ thị (Graph Retrieval)**: Một câu truy vấn Cypher được sinh ra tự động để kéo đúng các mạng lưới đồ thị thỏa mãn điều kiện nhân khẩu học đó ra.
3. **Sinh văn bản Tăng cường (Augmented Generation)**: LLM tổng hợp các đoạn text bình luận chất lượng cao vừa được lấy ra từ đồ thị, và tổng hợp lại thành một lời khuyên tư vấn mua sắm cực kỳ tự nhiên và mang tính cá nhân hóa cao.
