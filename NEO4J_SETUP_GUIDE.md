# HƯỚNG DẪN CÀI ĐẶT & TRIỂN KHAI NEO4J GRAPH EXTENSION (TÙY CHỌN)
**Phần mở rộng:** Triển khai Đồ thị Tri thức (Knowledge Graph) với Neo4j  
**Môn học:** Phát triển các hệ thống thông minh (Assignment 02)

---

> [!NOTE]
> Đây là **Phần Mở Rộng Tùy Chọn (Optional Extension)** nhằm nâng cao kiến trúc hệ thống bằng cách mô hình hóa quan hệ thực thể (Graph Relations) giữa Khách hàng, Nhận xét, Sản phẩm và Danh mục hàng hóa.  
> Các chức năng cốt lõi của Assignment 02 (3 Notebooks, ML Pipelines, REST API, Web & Mobile) đã hoàn thành độc lập 100%.

---

## 1. Tải và Cài Đặt Neo4j

### Lựa chọn A: Dùng Docker (Khuyên dùng trên Linux)
Nếu máy bạn có Docker, chỉ cần chạy 1 câu lệnh để khởi chạy Neo4j:
```bash
docker run \
    --name neo4j-assignment02 \
    -p 7474:7474 -p 7687:7687 \
    -d \
    -e NEO4J_AUTH=neo4j/password123 \
    neo4j:latest
```

### Lựa chọn B: Dùng Neo4j Desktop
1. Tải Neo4j Desktop cho Linux từ trang chủ: [https://neo4j.com/download/](https://neo4j.com/download/)
2. Cài đặt AppImage hoặc .deb.
3. Mở Neo4j Desktop, chọn **New Project** $\rightarrow$ **Add Local DBMS**.
4. Đặt tên: `Assignment02-Graph`.
5. Đặt mật khẩu: `password123`.
6. Bấm **Start** để chạy Database.

---

## 2. Thông Tin Kết Nối (Connection Details)

- **Giao thức Bolt:** `bolt://localhost:7687`
- **Neo4j Browser (Giao diện Web):** `http://localhost:7474`
- **Username mặc định:** `neo4j`
- **Password:** `password123`

Cài đặt thư viện Python Neo4j Driver trong môi trường `ai-env`:
```bash
conda activate ai-env
pip install neo4j
```

---

## 3. Cấu Trúc Đồ Thị Tri Thức (Graph Schema)

Mô hình hóa dữ liệu E-Commerce thành các nút (Nodes) và quan hệ (Relationships):
```text
(:Customer {id, age})
       │
   [:WROTE]
       ▼
(:Review {id, rating, recommended, text})
       │
   [:ABOUT]
       ▼
(:Product {id})
       │
 [:BELONGS_TO]
       ▼
(:Category {name})
       │
  [:PART_OF]
       ▼
(:Department {name})
```

---

## 4. Nạp Dữ Liệu & Khởi Tạo Ràng Buộc (Cypher Ingestion)

Mở **Neo4j Browser** tại `http://localhost:7474` và chạy tệp kịch bản Cypher được cung cấp sẵn tại `scripts/import_graph.cypher`:

1. **Tạo ràng buộc duy nhất (Constraints):**
   ```cypher
   CREATE CONSTRAINT customer_id_unique IF NOT EXISTS FOR (c:Customer) REQUIRE c.id IS UNIQUE;
   CREATE CONSTRAINT product_id_unique IF NOT EXISTS FOR (p:Product) REQUIRE p.id IS UNIQUE;
   CREATE CONSTRAINT category_name_unique IF NOT EXISTS FOR (cat:Category) REQUIRE cat.name IS UNIQUE;
   ```

2. **Chạy kịch bản tự động bằng Python:**
   ```bash
   python scripts/neo4j_demo.py
   ```
   Kịch bản sẽ tự động trích xuất mẫu đại diện (representative subset) từ bộ dữ liệu `Womens Clothing E-Commerce Reviews.csv` và đưa vào Neo4j.

---

## 5. Các Câu Truy Vấn Cypher Phân Tích Thực Tế

### Truy vấn 1: Tìm các sản phẩm được đề xuất nhiều nhất có đánh giá 5 sao
```cypher
MATCH (p:Product)<-[:ABOUT]-(r:Review)
WHERE r.rating = 5 AND r.recommended = 1
RETURN p.id AS MaSanPham, count(r) AS SoLuongDanhGia5Sao
ORDER BY SoLuongDanhGia5Sao DESC
LIMIT 10;
```

### Truy vấn 2: Phân tích độ tuổi khách hàng trung bình theo từng ngành hàng
```cypher
MATCH (c:Customer)-[:WROTE]->(r:Review)-[:ABOUT]->(p:Product)-[:BELONGS_TO]->(cat:Category)
WHERE r.recommended = 1
RETURN cat.name AS NganhHang, round(avg(c.age), 1) AS TuoiTrungBinh, count(r) AS TongDeXuat
ORDER BY TongDeXuat DESC;
```

### Truy vấn 3: Truy vết phản hồi tiêu cực để cảnh báo kiểm soát chất lượng
```cypher
MATCH (c:Customer)-[:WROTE]->(r:Review)-[:ABOUT]->(p:Product)
WHERE r.rating <= 2 AND r.recommended = 0
RETURN p.id AS MaSanPham, r.text AS NoiDungPhanNan, c.age AS TuoiKhachHang
LIMIT 10;
```

---

## 6. Hướng Dẫn Chụp Ảnh Minh Chứng (Nếu Thầy Yêu Cầu Demo Neo4j)

1. Mở Neo4j Browser tại `http://localhost:7474`.
2. Chạy câu truy vấn hiển thị đồ thị trực quan:
   ```cypher
   MATCH path = (c:Customer)-[:WROTE]->(r:Review)-[:ABOUT]->(p:Product)-[:BELONGS_TO]->(cat:Category)
   RETURN path LIMIT 25;
   ```
3. Chụp lại giao diện mạng đồ thị các node bóng tròn nhiều màu sắc nối với nhau bằng các cạnh mũi tên.
4. Lưu ảnh vào: `screenshots/neo4j_optional/graph_visualization.png`.
5. Đưa ảnh vào **Phụ Lục (Appendix) / Chương Mở Rộng** của báo cáo.
