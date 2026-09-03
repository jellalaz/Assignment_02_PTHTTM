import docx

def add_lan_note_to_docx(filepath):
    doc = docx.Document(filepath)
    fixes = 0
    
    for p in doc.paragraphs:
        if "Điện thoại và máy tính chỉ cần kết nối cùng một mạng Wi-Fi." in p.text:
            # We found the paragraph in chapter 6.6
            p.text = p.text.split("Lưu ý quan trọng")[0] + " Lưu ý quan trọng: Máy chủ bắt buộc phải chạy ở host 0.0.0.0. Nếu khởi chạy bằng 127.0.0.1 (localhost), các máy khác trong mạng sẽ không thể truy cập được. Người dùng trên mạng LAN phải gõ IP thực của máy chủ (ví dụ 172.18.2.105:8000) thay vì 127.0.0.1."
            # re-apply font
            for run in p.runs:
                run.font.name = 'Times New Roman'
            fixes += 1
            
        if "Sử dụng URL tương đối" in p.text:
            p.text = p.text.split("Lưu ý:")[0] + " Lưu ý: 127.0.0.1 chỉ dùng được trên máy cài đặt; máy khác truy cập phải dùng IP LAN (VD: 172.18.2.105)."
            for run in p.runs:
                run.font.name = 'Times New Roman'
            fixes += 1

    doc.save(filepath)
    return fixes

if __name__ == '__main__':
    doc_path = '/home/jellalaz/Documents/Jellalaz/DATA_CODE/PYTHON/Assignment_02/report/Baocao.docx'
    fixes = add_lan_note_to_docx(doc_path)
    print(f"Made {fixes} additions to clarify 127.0.0.1 access.")
