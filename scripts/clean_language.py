import glob
import re

for filepath in glob.glob("scripts/report_builder/ch*.py"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Remove overused phrases
    replacements = {
        "Đoạn mã xây dựng": "Sử dụng",
        "Đoạn mã sử dụng": "Áp dụng",
        "Đoạn mã này dùng để": "Nhằm",
        "Đây là một bước quan trọng trong quy trình": "Bước này giúp",
        "Điều này cho thấy mô hình có khả năng": "Mô hình thể hiện khả năng",
        "Có thể thấy rằng": "Thực tế cho thấy",
        "Nhìn chung có thể thấy": "Nhìn chung,",
        "Kết quả trên cho thấy": "Kết quả cho thấy",
        "Đoạn mã tính toán": "Tính toán",
        "Đoạn mã lọc ra": "Lọc ra",
        "Đoạn mã trực quan hóa": "Trực quan hóa",
        "Đoạn mã kiểm định năng lực": "Kiểm định",
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
        content = content.replace(old.lower(), new.lower())

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
