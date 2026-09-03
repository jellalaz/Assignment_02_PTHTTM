# Hướng Dẫn Truy Cập Giao Diện Mobile Qua Mạng Cục Bộ (LAN)
**Hệ thống:** Responsive Mobile Web Client (Assignment 02 — Intelligent System Development)

---

## 1. Kiến Trúc Hoạt Động Của Mobile Client

Theo yêu cầu chính thức của môn học và hướng triển khai thực tế:
```text
Smartphone Browser (iOS / Android)
            │
            ▼  (Wi-Fi / LAN)
FastAPI Server (bind 0.0.0.0:8000)
            │
            ▼
Saved Preprocessing Pipelines (.joblib)
            │
            ▼
Saved Machine Learning Models (.joblib)
            │
            ▼
JSON Prediction & Confidence Response
            │
            ▼
Responsive Mobile Web UI (Hiển thị kết quả trên điện thoại)
```

Giao diện Web được thiết kế theo nguyên chuẩn **Responsive Mobile-First**:
- Tự động co giãn theo khung nhìn điện thoại thông minh (chuẩn iPhone/Android viewport: `390 x 844`).
- Không có hiện tượng tràn khung ngang (no horizontal overflow).
- Các nút bấm, trường nhập liệu được tối ưu cảm ứng (touch-friendly targets).
- Các request API sử dụng đường dẫn tương đối (`/predict/diabetes`, `/predict/house`, `/predict/ecommerce`), bảo đảm thiết bị di động gọi API về máy chủ host thông qua mạng LAN mà không bao giờ bị lỗi do hardcoded `localhost`.

---

## 2. Các Bước Khởi Chạy Và Kết Nối Từ Điện Thoại

### Bước 1: Khởi chạy Server trên máy tính (Host)
Mở terminal trong thư mục dự án và chạy:
```bash
# Kích hoạt conda environment
conda activate ai-env

# Di chuyển vào thư mục Assignment_02
cd /home/jellalaz/Documents/Jellalaz/DATA_CODE/PYTHON/Assignment_02

# Chạy server bind trên tất cả địa chỉ mạng (0.0.0.0)
PYTHONPATH=. /home/jellalaz/miniconda3/envs/ai-env/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### Bước 2: Xác định địa chỉ IP mạng nội bộ (LAN IP)
Trên máy Linux host, chạy lệnh:
```bash
hostname -I
```
Kết quả thực tế của máy bạn: **`192.168.0.105`**

### Bước 3: Kết nối điện thoại cùng mạng Wi-Fi
- Bảo đảm điện thoại của bạn đang kết nối vào **cùng một mạng Wi-Fi** với laptop/PC chạy server.
- Mở trình duyệt trên điện thoại (Safari trên iOS hoặc Chrome trên Android).
- Nhập URL sau vào thanh địa chỉ:
  ```text
  http://192.168.0.105:8000/
  ```

---

## 3. Xử Lý Tường Lửa (Troubleshooting Firewall)

Nếu trên điện thoại báo không kết nối được hoặc timeout:
1. **Kiểm tra UFW trên Linux:**
   ```bash
   sudo ufw allow 8000/tcp
   sudo ufw reload
   ```
2. **Kiểm tra iptables:**
   ```bash
   sudo iptables -I INPUT -p tcp --dport 8000 -j ACCEPT
   ```
3. **Thử ping:**
   Từ điện thoại (nếu có app Terminal/Ping), ping thử địa chỉ `192.168.0.105` để chắc chắn hai máy nhìn thấy nhau trong mạng LAN.

---

## 4. Các Màn Hình Minh Chứng Đã Được Hệ Thống Tự Động Chụp

Hệ thống đã tự động mô phỏng khung nhìn di động chuẩn (`390 x 844`) bằng Google Chrome headless và lưu ảnh thật tại:

| Tên Tệp Ảnh | Khung Nhìn / Nội Dung | Vị Trí Đưa Vào Báo Cáo |
|---|---|---|
| `screenshots/mobile/mobile_home.png` | Màn hình chính Responsive trên điện thoại | Chương 6 — Triển khai Mobile |
| `screenshots/mobile/diabetes_mobile.png` | Kết quả chẩn đoán Tiểu đường trên điện thoại | Chương 6 / Chương 7 (Mobile Demo) |
| `screenshots/mobile/house_mobile.png` | Định giá nhà trực tiếp trên điện thoại | Chương 6 / Chương 8 (Mobile Demo) |
| `screenshots/mobile/ecommerce_mobile.png` | Dự đoán đề xuất sản phẩm trên điện thoại | Chương 6 / Chương 9 (Mobile Demo) |

---

## 5. Tuyên Bố Trung Thực Về Mobile Client Trong Báo Cáo & Checklist

Trong báo cáo kỹ thuật và `FINAL_CHECKLIST.md`, tình trạng triển khai được ghi nhận rõ ràng:
- **Responsive Mobile Web Client qua LAN:** **DONE** (Đã chạy thực tế, kiểm thử responsive 390x844, chụp ảnh thật từ web server đang chạy).
- **Native Android / Flutter Application:** **NOT IMPLEMENTED** (Theo chỉ đạo không làm Flutter native, thay thế hoàn toàn bằng Responsive Mobile Web Client truy cập qua mạng LAN).
