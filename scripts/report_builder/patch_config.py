import re

with open("scripts/report_builder/config.py", "r", encoding="utf-8") as f:
    content = f.read()

# Patch add_figure_with_notes
old_fig = """    p_obs_title = doc.add_paragraph()
    p_obs_title.paragraph_format.space_before = Pt(2)
    p_obs_title.paragraph_format.space_after = Pt(2)
    p_obs_title.paragraph_format.keep_with_next = True
    r_ot = p_obs_title.add_run("Nhận xét và phân tích biểu đồ:")
    r_ot.font.name = "Times New Roman"
    r_ot.font.size = Pt(12)
    r_ot.font.bold = True
    r_ot.font.color.rgb = COLOR_DARK_BLUE
    
    for item in observations:
        add_bullet_p(doc, item, bold_prefix="Nhận xét: " if item == observations[0] else None)
    if explanation:
        add_bullet_p(doc, explanation, bold_prefix="Giải thích: ")
    if ml_implication:
        add_bullet_p(doc, ml_implication, bold_prefix="Ý nghĩa đối với mô hình / ML: ")
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_after = Pt(4)"""

new_fig = """    for item in observations:
        add_body_p(doc, item)
    if explanation:
        add_body_p(doc, explanation)
    if ml_implication:
        add_body_p(doc, ml_implication)
    
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_after = Pt(4)"""

content = content.replace(old_fig, new_fig)


# Patch add_code_snippet_with_notes
old_code = """    p_desc = doc.add_paragraph()
    p_desc.paragraph_format.space_before = Pt(2)
    p_desc.paragraph_format.space_after = Pt(2)
    r_dt = p_desc.add_run("Mô tả:")
    r_dt.font.name = "Times New Roman"
    r_dt.font.size = Pt(11.5)
    r_dt.font.bold = True
    r_dt.font.italic = True
    
    for item in description_items:
        add_bullet_p(doc, item)
        
    if source_file:
        p_src = doc.add_paragraph()
        p_src.paragraph_format.left_indent = Inches(0.25)
        p_src.paragraph_format.space_before = Pt(0)
        p_src.paragraph_format.space_after = Pt(4)
        r_src_label = p_src.add_run("Nguồn: ")
        r_src_label.font.name = "Times New Roman"
        r_src_label.font.size = Pt(11)
        r_src_label.font.italic = True
        
        r_src_code = p_src.add_run(source_file)
        r_src_code.font.name = "Consolas"
        r_src_code.font.size = Pt(10)
        r_src_code.font.color.rgb = COLOR_DARK_GRAY
        
    doc.add_paragraph().paragraph_format.space_after = Pt(4)"""

new_code = """    for item in description_items:
        add_body_p(doc, item)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(4)"""

content = content.replace(old_code, new_code)

with open("scripts/report_builder/config.py", "w", encoding="utf-8") as f:
    f.write(content)
