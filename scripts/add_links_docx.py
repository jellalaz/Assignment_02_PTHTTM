import docx

def add_links_to_docx(filepath):
    doc = docx.Document(filepath)
    fixes = 0
    
    for p in doc.paragraphs:
        if "Điện thoại và máy tính chỉ cần kết nối cùng một mạng Wi-Fi." in p.text:
            p.text = "Giao diện Web/App Mobile qua LAN có thể truy cập nội bộ tại địa chỉ: http://172.18.2.105:8000/ \n" \
                     "Mã nguồn toàn bộ dự án đã được lưu trữ và triển khai trên GitHub tại địa chỉ: https://github.com/jellalaz/Assignment_02_PTHTTM"
            for run in p.runs:
                run.font.name = 'Times New Roman'
            fixes += 1
            
        if "Sử dụng URL tương đối" in p.text:
            p.text = p.text.split("Lưu ý:")[0]
            for run in p.runs:
                run.font.name = 'Times New Roman'

    doc.save(filepath)
    return fixes

if __name__ == '__main__':
    doc_path = '/home/jellalaz/Documents/Jellalaz/DATA_CODE/PYTHON/Assignment_02/report/Baocao.docx'
    fixes = add_links_to_docx(doc_path)
    print(f"Made {fixes} additions for GitHub and App links.")
