# -*- coding: utf-8 -*-
"""
build_docx.py - Compiles Final_Project_Report.docx with strict university thesis styling
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from metadata import *
from ch1_intro import CHAPTER_1_TITLE, SECTIONS as CH1_SECTIONS
from ch2_literature import CHAPTER_2_TITLE, SECTIONS as CH2_SECTIONS, TABLE_2_1_DATA
from ch3_methodology import CHAPTER_3_TITLE, SECTIONS as CH3_SECTIONS
from ch4_design import CHAPTER_4_TITLE, SECTIONS as CH4_SECTIONS, TABLE_4_1_DATA
from ch5_implementation import CHAPTER_5_TITLE, SECTIONS as CH5_SECTIONS
from ch6_results import CHAPTER_6_TITLE, SECTIONS as CH6_SECTIONS, TABLE_6_1_DATA, TABLE_6_2_DATA, TABLE_6_3_DATA, TABLE_6_4_DATA, TABLE_6_5_DATA, TABLE_6_6_DATA
from ch7_conclusion import CHAPTER_7_TITLE, SECTIONS as CH7_SECTIONS
from references_appendices import (
    REFERENCES_LIST,
    APPENDIX_A1, APPENDIX_A2, APPENDIX_A3, APPENDIX_A4,
    APPENDIX_A5, APPENDIX_A6, APPENDIX_A7, APPENDIX_A8,
    TECHNICAL_BIOGRAPHY
)

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_table_to_doc(doc, table_data):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(table_data["title"])
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(30, 41, 59)
    
    headers = table_data["headers"]
    rows = table_data["rows"]
    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    
    # Format Header Row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "1F4E79") # Professional Navy Blue
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=150, right=150)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            
    # Format Body Rows
    for row_idx, row_vals in enumerate(rows):
        row_cells = table.rows[row_idx + 1].cells
        bg_color = "F2F5F8" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(row_vals):
            row_cells[col_idx].text = str(val)
            set_cell_background(row_cells[col_idx], bg_color)
            set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=120, right=120)
            p = row_cells[col_idx].paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(30, 41, 59)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(15, 23, 42)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(13.5)
    run.font.bold = True
    run.font.color.rgb = RGBColor(30, 58, 138)
    return p

def add_body_paragraph(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.5
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(30, 41, 59)
    return p

def build_docx_report(output_path):
    doc = Document()
    
    # Configure Academic Thesis Margins: Left 1.5 in (Binding), Right 1.0 in, Top 1.0 in, Bottom 1.0 in
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.5)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)  # A4
        section.page_height = Inches(11.69) # A4
        
        # Header setup
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Autonomous Multimodal Industrial Monitoring System (ESP32-S3 / Edge AI)")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.italic = True
        hrun.font.color.rgb = RGBColor(100, 116, 139)
        
        # Footer setup
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Department of Electronics and Communication Engineering")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(100, 116, 139)
        
    # ==================== 1. TITLE PAGE ====================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(36)
    p_title.paragraph_format.space_after = Pt(12)
    r = p_title.add_run(TITLE)
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = RGBColor(15, 23, 42)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(24)
    r = p_sub.add_run("A PROJECT REPORT\nSubmitted in partial fulfillment of the requirements for the award of the degree of")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.italic = True
    
    p_deg = doc.add_paragraph()
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_deg.paragraph_format.space_after = Pt(36)
    r = p_deg.add_run(f"{DEGREE}\nIN\n{BRANCH}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    
    p_cand = doc.add_paragraph()
    p_cand.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cand.paragraph_format.space_after = Pt(24)
    r = p_cand.add_run(f"Submitted by:\n{PLACEHOLDERS['STUDENT_NAME']}\n(Registration No: {PLACEHOLDERS['REG_NO']})")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    
    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_after = Pt(36)
    r = p_guide.add_run(f"Under the Guidance of:\n{PLACEHOLDERS['GUIDE_NAME']}\n{PLACEHOLDERS['GUIDE_DESIGNATION']}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_inst.add_run(f"{PLACEHOLDERS['DEPARTMENT']}\n{PLACEHOLDERS['COLLEGE_NAME']}\n{PLACEHOLDERS['COLLEGE_ADDRESS']}\nAffiliated to {PLACEHOLDERS['UNIVERSITY']}\nAcademic Year: {PLACEHOLDERS['ACADEMIC_YEAR']}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    
    doc.add_page_break()
    
    # ==================== 2. CERTIFICATE ====================
    add_heading_1(doc, "CERTIFICATE")
    add_body_paragraph(doc, CERTIFICATE_TEXT)
    
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(48)
    r = p_sig.add_run(f"Internal Project Guide: {PLACEHOLDERS['GUIDE_NAME']}\n{PLACEHOLDERS['GUIDE_DESIGNATION']}\n\n\n\nHead of the Department: {PLACEHOLDERS['HOD_NAME']}\n{PLACEHOLDERS['HOD_DESIGNATION']}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    
    doc.add_page_break()
    
    # ==================== 3. DECLARATION ====================
    add_heading_1(doc, "DECLARATION")
    add_body_paragraph(doc, DECLARATION_TEXT)
    
    p_decl = doc.add_paragraph()
    p_decl.paragraph_format.space_before = Pt(48)
    r = p_decl.add_run(f"Place: ____________________\nDate:  ____________________\n\n\nCandidate Signature: ____________________\n{PLACEHOLDERS['STUDENT_NAME']}\n(Reg. No: {PLACEHOLDERS['REG_NO']})")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    
    doc.add_page_break()
    
    # ==================== 4. ACKNOWLEDGEMENT ====================
    add_heading_1(doc, "ACKNOWLEDGEMENT")
    for para in ACKNOWLEDGEMENT_TEXT.split("\n\n"):
        add_body_paragraph(doc, para)
    doc.add_page_break()
    
    # ==================== 5. ABSTRACT ====================
    add_heading_1(doc, "ABSTRACT")
    for para in ABSTRACT_TEXT.split("\n\n"):
        add_body_paragraph(doc, para)
    doc.add_page_break()
    
    # ==================== 6. TABLE OF CONTENTS ====================
    add_heading_1(doc, "TABLE OF CONTENTS")
    toc_lines = [
        "Certificate", "Declaration", "Acknowledgement", "Abstract",
        "Table of Contents", "List of Figures", "List of Tables", "List of Abbreviations",
        "Chapter 1: Introduction",
        "  1.1 Introduction", "    1.1.1 Overview of Industrial 4.0 & Predictive Maintenance", "    1.1.2 System Technologies",
        "  1.2 Objectives", "  1.3 Project Description", "  1.4 Scope of the Project", "  1.5 Applications of the Project",
        "Chapter 2: Literature Survey",
        "  2.1 Introduction", "  2.2 Existing Research on Industrial IoT Monitoring", "  2.3 MEMS-Based Vibration Monitoring",
        "  2.4 Temperature Monitoring in Industrial Motors", "  2.5 Current-Based Motor Fault Detection", "  2.6 Piezoelectric Energy Harvesting",
        "  2.7 Edge AI and TinyML in Predictive Maintenance", "  2.8 Adaptive Wireless Communication", "  2.9 Research Gap", "  2.10 Literature Survey Summary",
        "Chapter 3: Problem Definition and Methodology",
        "  3.1 Problem Definition", "  3.2 Existing System", "  3.3 Limitations of the Existing System", "  3.4 Proposed System",
        "  3.5 Advantages of the Proposed System", "  3.6 Methodology", "  3.7 System Architecture", "  3.8 Working Principle",
        "Chapter 4: Design Overview",
        "  4.1 Design Overview", "  4.2 Three-Tier System Architecture", "  4.3 Data Flow Diagram", "  4.4 Hardware Architecture",
        "  4.5 Software Architecture", "  4.6 Database Design", "  4.7 Project Requirements", "  4.8 Sensor Interfacing Design",
        "  4.9 Communication Protocol Design", "  4.10 Database Schema Design",
        "Chapter 5: Implementation",
        "  5.1 Software Development", "  5.2 Hardware Setup", "  5.3 Sensor Data Collection", "  5.4 Data Processing",
        "  5.5 Fault Detection Implementation", "  5.6 Docker Containerisation", "  5.7 System Integration", "  5.8 Performance Evaluation",
        "Chapter 6: Results and Discussion",
        "  6.1 Experimental Setup", "  6.2 Real-Time Monitoring Results", "  6.3 Vibration Analysis Results", "  6.4 Temperature Monitoring Results",
        "  6.5 Current Monitoring Results", "  6.6 Energy Harvesting Investigation Results", "  6.7 Fault Detection Performance",
        "  6.8 System Latency and Performance", "  6.9 Discussion",
        "Chapter 7: Conclusion and Future Scope",
        "  7.1 Conclusion", "  7.2 Future Scope",
        "References", "Appendices (A1 - A8)", "Technical Biography"
    ]
    for item in toc_lines:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(item)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        if item.startswith("Chapter") or item in ["Certificate", "Declaration", "Acknowledgement", "Abstract", "References", "Appendices (A1 - A8)", "Technical Biography"]:
            r.font.bold = True
    doc.add_page_break()
    
    # ==================== CHAPTER 1 ====================
    add_heading_1(doc, CHAPTER_1_TITLE)
    for s in CH1_SECTIONS:
        add_heading_2(doc, f"{s['number']} {s['title']}")
        for para in s["content"].split("\n\n"):
            add_body_paragraph(doc, para)
    doc.add_page_break()
    
    # ==================== CHAPTER 2 ====================
    add_heading_1(doc, CHAPTER_2_TITLE)
    for s in CH2_SECTIONS:
        add_heading_2(doc, f"{s['number']} {s['title']}")
        for para in s["content"].split("\n\n"):
            add_body_paragraph(doc, para)
    add_table_to_doc(doc, TABLE_2_1_DATA)
    doc.add_page_break()
    
    # ==================== CHAPTER 3 ====================
    add_heading_1(doc, CHAPTER_3_TITLE)
    for s in CH3_SECTIONS:
        add_heading_2(doc, f"{s['number']} {s['title']}")
        for para in s["content"].split("\n\n"):
            add_body_paragraph(doc, para)
    doc.add_page_break()
    
    # ==================== CHAPTER 4 ====================
    add_heading_1(doc, CHAPTER_4_TITLE)
    for s in CH4_SECTIONS:
        add_heading_2(doc, f"{s['number']} {s['title']}")
        for para in s["content"].split("\n\n"):
            add_body_paragraph(doc, para)
    add_table_to_doc(doc, TABLE_4_1_DATA)
    doc.add_page_break()
    
    # ==================== CHAPTER 5 ====================
    add_heading_1(doc, CHAPTER_5_TITLE)
    for s in CH5_SECTIONS:
        add_heading_2(doc, f"{s['number']} {s['title']}")
        for para in s["content"].split("\n\n"):
            add_body_paragraph(doc, para)
    doc.add_page_break()
    
    # ==================== CHAPTER 6 ====================
    add_heading_1(doc, CHAPTER_6_TITLE)
    for s in CH6_SECTIONS:
        add_heading_2(doc, f"{s['number']} {s['title']}")
        for para in s["content"].split("\n\n"):
            add_body_paragraph(doc, para)
    add_table_to_doc(doc, TABLE_6_1_DATA)
    add_table_to_doc(doc, TABLE_6_2_DATA)
    add_table_to_doc(doc, TABLE_6_3_DATA)
    add_table_to_doc(doc, TABLE_6_4_DATA)
    add_table_to_doc(doc, TABLE_6_5_DATA)
    add_table_to_doc(doc, TABLE_6_6_DATA)
    doc.add_page_break()
    
    # ==================== CHAPTER 7 ====================
    add_heading_1(doc, CHAPTER_7_TITLE)
    for s in CH7_SECTIONS:
        add_heading_2(doc, f"{s['number']} {s['title']}")
        for para in s["content"].split("\n\n"):
            add_body_paragraph(doc, para)
    doc.add_page_break()
    
    # ==================== REFERENCES ====================
    add_heading_1(doc, "REFERENCES")
    for ref in REFERENCES_LIST:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(ref)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
    doc.add_page_break()
    
    # ==================== APPENDICES ====================
    for app in [APPENDIX_A1, APPENDIX_A2, APPENDIX_A3, APPENDIX_A4, APPENDIX_A5, APPENDIX_A6, APPENDIX_A7, APPENDIX_A8]:
        add_heading_1(doc, app["title"])
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.05
        r = p.add_run(app["content"])
        r.font.name = "Consolas"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(30, 41, 59)
        doc.add_page_break()
        
    # ==================== TECHNICAL BIOGRAPHY ====================
    add_heading_1(doc, "TECHNICAL BIOGRAPHY")
    for para in TECHNICAL_BIOGRAPHY.replace("# TECHNICAL BIOGRAPHY\n\n", "").split("\n\n"):
        add_body_paragraph(doc, para)
        
    doc.save(output_path)
    print(f"[SUCCESS] Generated DOCX report at: {output_path}")

if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "..", "Final_Project_Report.docx")
    build_docx_report(os.path.abspath(out_file))
