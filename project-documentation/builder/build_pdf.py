# -*- coding: utf-8 -*-
"""
build_pdf.py - Compiles Final_Project_Report.pdf using ReportLab with embedded screenshots
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted, KeepTogether, Image
)
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT

from metadata import *
from ch1_intro import CHAPTER_1_TITLE, SECTIONS as CH1_SECTIONS
from ch2_literature import CHAPTER_2_TITLE, SECTIONS as CH2_SECTIONS, TABLE_2_1_DATA
from ch3_methodology import CHAPTER_3_TITLE, SECTIONS as CH3_SECTIONS
from ch4_design import CHAPTER_4_TITLE, SECTIONS as CH4_SECTIONS, TABLE_4_1_DATA
from ch5_implementation import CHAPTER_5_TITLE, SECTIONS as CH5_SECTIONS
from ch6_results import (
    CHAPTER_6_TITLE, SECTIONS as CH6_SECTIONS,
    FIGURES_6_DATA,
    TABLE_6_1_DATA, TABLE_6_2_DATA, TABLE_6_3_DATA, TABLE_6_4_DATA, TABLE_6_5_DATA, TABLE_6_6_DATA
)
from ch7_conclusion import CHAPTER_7_TITLE, SECTIONS as CH7_SECTIONS
from references_appendices import (
    REFERENCES_LIST,
    APPENDIX_A1, APPENDIX_A2, APPENDIX_A3, APPENDIX_A4,
    APPENDIX_A5, APPENDIX_A6, APPENDIX_A7, APPENDIX_A8,
    TECHNICAL_BIOGRAPHY
)

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, total_pages):
        if self._pageNumber == 1:
            return # Skip title page decorations
            
        self.saveState()
        self.setFont("Times-Italic", 8.5)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (Top)
        self.drawRightString(A4[0] - 54, A4[1] - 36, "Autonomous Multimodal Industrial Monitoring System (ESP32-S3 / Edge AI)")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, A4[1] - 42, A4[0] - 54, A4[1] - 42)
        
        # Footer (Bottom)
        self.setFont("Times-Roman", 8.5)
        self.drawString(54, 36, "Department of Electronics and Communication Engineering")
        page_text = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(A4[0] - 54, 36, page_text)
        self.line(54, 48, A4[0] - 54, 48)
        
        self.restoreState()

def create_pdf_table(table_data, styles, col_widths=None):
    headers = table_data["headers"]
    rows = table_data["rows"]
    
    table_content = []
    
    # Format header row
    hdr_row = [Paragraph(f"<b><font color='white'>{h}</font></b>", styles["TableHeader"]) for h in headers]
    table_content.append(hdr_row)
    
    # Format body rows
    for r in rows:
        body_row = [Paragraph(str(cell), styles["TableCell"]) for cell in r]
        table_content.append(body_row)
        
    t = Table(table_content, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    return t

def build_pdf_report(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=54, # 0.75 in
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Academic Styles
    styles.add(ParagraphStyle(
        name='MainTitle',
        fontName='Times-Bold',
        fontSize=16,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=15
    ))
    styles.add(ParagraphStyle(
        name='TitleSub',
        fontName='Times-Italic',
        fontSize=11,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#334155"),
        spaceAfter=15
    ))
    styles.add(ParagraphStyle(
        name='TitleDegree',
        fontName='Times-Bold',
        fontSize=13,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=25
    ))
    styles.add(ParagraphStyle(
        name='TitleAuthor',
        fontName='Times-Roman',
        fontSize=11,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=20
    ))
    styles.add(ParagraphStyle(
        name='AcademicH1',
        fontName='Times-Bold',
        fontSize=15,
        leading=20,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#1F4E79"),
        spaceBefore=14,
        spaceAfter=10,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name='AcademicH2',
        fontName='Times-Bold',
        fontSize=12.5,
        leading=17,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name='AcademicBody',
        fontName='Times-Roman',
        fontSize=10.5,
        leading=15,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name='TableTitle',
        fontName='Times-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name='FigureCaption',
        fontName='Times-Italic',
        fontSize=8.5,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#475569"),
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.white
    ))
    styles.add(ParagraphStyle(
        name='TableCell',
        fontName='Times-Roman',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1E293B")
    ))
    styles.add(ParagraphStyle(
        name='ReferenceText',
        fontName='Times-Roman',
        fontSize=9,
        leading=13,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=5
    ))
    styles.add(ParagraphStyle(
        name='CodeSnippet',
        fontName='Courier',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#0F172A")
    ))
    
    story = []
    
    # ==================== 1. TITLE PAGE ====================
    story.append(Spacer(1, 20))
    story.append(Paragraph(TITLE, styles['MainTitle']))
    story.append(Paragraph("A PROJECT REPORT<br/><i>Submitted in partial fulfillment of the requirements for the award of the degree of</i>", styles['TitleSub']))
    story.append(Paragraph(f"{DEGREE}<br/>IN<br/>{BRANCH}", styles['TitleDegree']))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"<b>Submitted by:</b><br/><b>{PLACEHOLDERS['STUDENT_NAME']}</b><br/>(Registration No: <b>{PLACEHOLDERS['REG_NO']}</b>)", styles['TitleAuthor']))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"<b>Under the Guidance of:</b><br/><b>{PLACEHOLDERS['GUIDE_NAME']}</b><br/>{PLACEHOLDERS['GUIDE_DESIGNATION']}", styles['TitleAuthor']))
    story.append(Spacer(1, 15))
    story.append(Paragraph(f"<b>{PLACEHOLDERS['DEPARTMENT']}</b><br/><b>{PLACEHOLDERS['COLLEGE_NAME']}</b><br/>{PLACEHOLDERS['COLLEGE_ADDRESS']}<br/>Affiliated to <b>{PLACEHOLDERS['UNIVERSITY']}</b><br/>Academic Year: <b>{PLACEHOLDERS['ACADEMIC_YEAR']}</b>", styles['TitleAuthor']))
    story.append(PageBreak())
    
    # ==================== 2. CERTIFICATE ====================
    story.append(Paragraph("CERTIFICATE", styles['AcademicH1']))
    story.append(Paragraph(CERTIFICATE_TEXT, styles['AcademicBody']))
    story.append(Spacer(1, 40))
    story.append(Paragraph(f"<b>{PLACEHOLDERS['GUIDE_NAME']}</b><br/>Internal Project Guide<br/>{PLACEHOLDERS['GUIDE_DESIGNATION']}", styles['AcademicBody']))
    story.append(Spacer(1, 25))
    story.append(Paragraph(f"<b>{PLACEHOLDERS['HOD_NAME']}</b><br/>Head of the Department<br/>{PLACEHOLDERS['HOD_DESIGNATION']}", styles['AcademicBody']))
    story.append(PageBreak())
    
    # ==================== 3. DECLARATION ====================
    story.append(Paragraph("DECLARATION", styles['AcademicH1']))
    story.append(Paragraph(DECLARATION_TEXT, styles['AcademicBody']))
    story.append(Spacer(1, 40))
    story.append(Paragraph(f"Place: ____________________<br/>Date:  ____________________<br/><br/><b>{PLACEHOLDERS['STUDENT_NAME']}</b><br/>Registration No: {PLACEHOLDERS['REG_NO']}", styles['AcademicBody']))
    story.append(PageBreak())
    
    # ==================== 4. ACKNOWLEDGEMENT ====================
    story.append(Paragraph("ACKNOWLEDGEMENT", styles['AcademicH1']))
    for p in ACKNOWLEDGEMENT_TEXT.split("\n\n"):
        story.append(Paragraph(p, styles['AcademicBody']))
    story.append(PageBreak())
    
    # ==================== 5. ABSTRACT ====================
    story.append(Paragraph("ABSTRACT", styles['AcademicH1']))
    for p in ABSTRACT_TEXT.split("\n\n"):
        story.append(Paragraph(p, styles['AcademicBody']))
    story.append(PageBreak())
    
    # ==================== 6. TABLE OF CONTENTS ====================
    story.append(Paragraph("TABLE OF CONTENTS", styles['AcademicH1']))
    toc_items = [
        "<b>Certificate</b>", "<b>Declaration</b>", "<b>Acknowledgement</b>", "<b>Abstract</b>",
        "<b>Table of Contents</b>", "<b>List of Figures</b>", "<b>List of Tables</b>", "<b>List of Abbreviations</b>",
        "<b>Chapter 1: Introduction</b>",
        "&nbsp;&nbsp;&nbsp;&nbsp;1.1 Introduction", "&nbsp;&nbsp;&nbsp;&nbsp;1.1.1 Overview of Industrial 4.0 & Predictive Maintenance", "&nbsp;&nbsp;&nbsp;&nbsp;1.1.2 System Technologies",
        "&nbsp;&nbsp;&nbsp;&nbsp;1.2 Objectives", "&nbsp;&nbsp;&nbsp;&nbsp;1.3 Project Description", "&nbsp;&nbsp;&nbsp;&nbsp;1.4 Scope of the Project", "&nbsp;&nbsp;&nbsp;&nbsp;1.5 Applications of the Project",
        "<b>Chapter 2: Literature Survey</b>",
        "&nbsp;&nbsp;&nbsp;&nbsp;2.1 Introduction", "&nbsp;&nbsp;&nbsp;&nbsp;2.2 Existing Research on Industrial IoT Monitoring", "&nbsp;&nbsp;&nbsp;&nbsp;2.3 MEMS-Based Vibration Monitoring",
        "&nbsp;&nbsp;&nbsp;&nbsp;2.4 Temperature Monitoring in Industrial Motors", "&nbsp;&nbsp;&nbsp;&nbsp;2.5 Current-Based Motor Fault Detection", "&nbsp;&nbsp;&nbsp;&nbsp;2.6 Piezoelectric Energy Harvesting",
        "&nbsp;&nbsp;&nbsp;&nbsp;2.7 Edge AI and TinyML in Predictive Maintenance", "&nbsp;&nbsp;&nbsp;&nbsp;2.8 Adaptive Wireless Communication", "&nbsp;&nbsp;&nbsp;&nbsp;2.9 Research Gap", "&nbsp;&nbsp;&nbsp;&nbsp;2.10 Literature Survey Summary",
        "<b>Chapter 3: Problem Definition and Methodology</b>",
        "&nbsp;&nbsp;&nbsp;&nbsp;3.1 Problem Definition", "&nbsp;&nbsp;&nbsp;&nbsp;3.2 Existing System", "&nbsp;&nbsp;&nbsp;&nbsp;3.3 Limitations of the Existing System", "&nbsp;&nbsp;&nbsp;&nbsp;3.4 Proposed System",
        "&nbsp;&nbsp;&nbsp;&nbsp;3.5 Advantages of the Proposed System", "&nbsp;&nbsp;&nbsp;&nbsp;3.6 Methodology", "&nbsp;&nbsp;&nbsp;&nbsp;3.7 System Architecture", "&nbsp;&nbsp;&nbsp;&nbsp;3.8 Working Principle",
        "<b>Chapter 4: Design Overview</b>",
        "&nbsp;&nbsp;&nbsp;&nbsp;4.1 Design Overview", "&nbsp;&nbsp;&nbsp;&nbsp;4.2 Three-Tier System Architecture", "&nbsp;&nbsp;&nbsp;&nbsp;4.3 Data Flow Diagram", "&nbsp;&nbsp;&nbsp;&nbsp;4.4 Hardware Architecture",
        "&nbsp;&nbsp;&nbsp;&nbsp;4.5 Software Architecture", "&nbsp;&nbsp;&nbsp;&nbsp;4.6 Database Design", "&nbsp;&nbsp;&nbsp;&nbsp;4.7 Project Requirements", "&nbsp;&nbsp;&nbsp;&nbsp;4.8 Sensor Interfacing Design",
        "&nbsp;&nbsp;&nbsp;&nbsp;4.9 Communication Protocol Design", "&nbsp;&nbsp;&nbsp;&nbsp;4.10 Database Schema Design",
        "<b>Chapter 5: Implementation</b>",
        "&nbsp;&nbsp;&nbsp;&nbsp;5.1 Software Development", "&nbsp;&nbsp;&nbsp;&nbsp;5.2 Hardware Setup", "&nbsp;&nbsp;&nbsp;&nbsp;5.3 Sensor Data Collection", "&nbsp;&nbsp;&nbsp;&nbsp;5.4 Data Processing",
        "&nbsp;&nbsp;&nbsp;&nbsp;5.5 Fault Detection Implementation", "&nbsp;&nbsp;&nbsp;&nbsp;5.6 Docker Containerisation", "&nbsp;&nbsp;&nbsp;&nbsp;5.7 System Integration", "&nbsp;&nbsp;&nbsp;&nbsp;5.8 Performance Evaluation",
        "<b>Chapter 6: Results and Discussion</b>",
        "&nbsp;&nbsp;&nbsp;&nbsp;6.1 Experimental Setup", "&nbsp;&nbsp;&nbsp;&nbsp;6.2 Real-Time Monitoring Results & Dashboard Screenshots", "&nbsp;&nbsp;&nbsp;&nbsp;6.3 Vibration Analysis Results", "&nbsp;&nbsp;&nbsp;&nbsp;6.4 Temperature Monitoring Results",
        "&nbsp;&nbsp;&nbsp;&nbsp;6.5 Current Monitoring Results", "&nbsp;&nbsp;&nbsp;&nbsp;6.6 Energy Harvesting Investigation Results", "&nbsp;&nbsp;&nbsp;&nbsp;6.7 Fault Detection Performance",
        "&nbsp;&nbsp;&nbsp;&nbsp;6.8 System Latency and Performance", "&nbsp;&nbsp;&nbsp;&nbsp;6.9 Discussion",
        "<b>Chapter 7: Conclusion and Future Scope</b>",
        "&nbsp;&nbsp;&nbsp;&nbsp;7.1 Conclusion", "&nbsp;&nbsp;&nbsp;&nbsp;7.2 Future Scope",
        "<b>References</b>", "<b>Appendices (A1 - A8)</b>", "<b>Technical Biography</b>"
    ]
    for item in toc_items:
        story.append(Paragraph(item, styles['AcademicBody']))
    story.append(PageBreak())
    
    # ==================== CHAPTER 1 ====================
    story.append(Paragraph(CHAPTER_1_TITLE, styles['AcademicH1']))
    for s in CH1_SECTIONS:
        story.append(Paragraph(f"{s['number']} {s['title']}", styles['AcademicH2']))
        for p in s["content"].split("\n\n"):
            story.append(Paragraph(p, styles['AcademicBody']))
    story.append(PageBreak())
    
    # ==================== CHAPTER 2 ====================
    story.append(Paragraph(CHAPTER_2_TITLE, styles['AcademicH1']))
    for s in CH2_SECTIONS:
        story.append(Paragraph(f"{s['number']} {s['title']}", styles['AcademicH2']))
        for p in s["content"].split("\n\n"):
            story.append(Paragraph(p, styles['AcademicBody']))
    story.append(Paragraph(TABLE_2_1_DATA["title"], styles['TableTitle']))
    story.append(create_pdf_table(TABLE_2_1_DATA, styles, [100, 100, 140, 145]))
    story.append(PageBreak())
    
    # ==================== CHAPTER 3 ====================
    story.append(Paragraph(CHAPTER_3_TITLE, styles['AcademicH1']))
    for s in CH3_SECTIONS:
        story.append(Paragraph(f"{s['number']} {s['title']}", styles['AcademicH2']))
        for p in s["content"].split("\n\n"):
            story.append(Paragraph(p, styles['AcademicBody']))
    story.append(PageBreak())
    
    # ==================== CHAPTER 4 ====================
    story.append(Paragraph(CHAPTER_4_TITLE, styles['AcademicH1']))
    for s in CH4_SECTIONS:
        story.append(Paragraph(f"{s['number']} {s['title']}", styles['AcademicH2']))
        for p in s["content"].split("\n\n"):
            story.append(Paragraph(p, styles['AcademicBody']))
    story.append(Paragraph(TABLE_4_1_DATA["title"], styles['TableTitle']))
    story.append(create_pdf_table(TABLE_4_1_DATA, styles, [65, 95, 95, 110, 120]))
    story.append(PageBreak())
    
    # ==================== CHAPTER 5 ====================
    story.append(Paragraph(CHAPTER_5_TITLE, styles['AcademicH1']))
    for s in CH5_SECTIONS:
        story.append(Paragraph(f"{s['number']} {s['title']}", styles['AcademicH2']))
        for p in s["content"].split("\n\n"):
            story.append(Paragraph(p, styles['AcademicBody']))
    story.append(PageBreak())
    
    # ==================== CHAPTER 6 ====================
    story.append(Paragraph(CHAPTER_6_TITLE, styles['AcademicH1']))
    screenshots_dir = os.path.join(os.path.dirname(__file__), "..", "screenshots")
    for s in CH6_SECTIONS:
        story.append(Paragraph(f"{s['number']} {s['title']}", styles['AcademicH2']))
        for p in s["content"].split("\n\n"):
            story.append(Paragraph(p, styles['AcademicBody']))
            
        # Embed screenshots under section 6.2
        if s["number"] == "6.2":
            for fig in FIGURES_6_DATA:
                img_path = os.path.join(screenshots_dir, fig["file"])
                if os.path.exists(img_path):
                    story.append(Spacer(1, 10))
                    story.append(Image(img_path, width=460, height=258.75))
                    story.append(Spacer(1, 3))
                    story.append(Paragraph(fig["caption"], styles['FigureCaption']))
                    story.append(Spacer(1, 12))
            
    story.append(Paragraph(TABLE_6_1_DATA["title"], styles['TableTitle']))
    story.append(create_pdf_table(TABLE_6_1_DATA, styles, [110, 60, 60, 65, 75, 75, 40]))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph(TABLE_6_2_DATA["title"], styles['TableTitle']))
    story.append(create_pdf_table(TABLE_6_2_DATA, styles, [95, 65, 70, 75, 80, 100]))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph(TABLE_6_3_DATA["title"], styles['TableTitle']))
    story.append(create_pdf_table(TABLE_6_3_DATA, styles, [95, 80, 75, 75, 80, 80]))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph(TABLE_6_4_DATA["title"], styles['TableTitle']))
    story.append(create_pdf_table(TABLE_6_4_DATA, styles, [110, 130, 110, 135]))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph(TABLE_6_5_DATA["title"], styles['TableTitle']))
    story.append(create_pdf_table(TABLE_6_5_DATA, styles, [90, 215, 85, 95]))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph(TABLE_6_6_DATA["title"], styles['TableTitle']))
    story.append(create_pdf_table(TABLE_6_6_DATA, styles, [110, 110, 130, 135]))
    story.append(PageBreak())
    
    # ==================== CHAPTER 7 ====================
    story.append(Paragraph(CHAPTER_7_TITLE, styles['AcademicH1']))
    for s in CH7_SECTIONS:
        story.append(Paragraph(f"{s['number']} {s['title']}", styles['AcademicH2']))
        for p in s["content"].split("\n\n"):
            story.append(Paragraph(p, styles['AcademicBody']))
    story.append(PageBreak())
    
    # ==================== REFERENCES ====================
    story.append(Paragraph("REFERENCES", styles['AcademicH1']))
    for ref in REFERENCES_LIST:
        story.append(Paragraph(ref, styles['ReferenceText']))
    story.append(PageBreak())
    
    # ==================== APPENDICES ====================
    for app in [APPENDIX_A1, APPENDIX_A2, APPENDIX_A3, APPENDIX_A4, APPENDIX_A5, APPENDIX_A6, APPENDIX_A7, APPENDIX_A8]:
        story.append(Paragraph(app["title"], styles['AcademicH1']))
        story.append(Preformatted(app["content"], styles['CodeSnippet']))
        story.append(PageBreak())
        
    # ==================== TECHNICAL BIOGRAPHY ====================
    story.append(Paragraph("TECHNICAL BIOGRAPHY", styles['AcademicH1']))
    for p in TECHNICAL_BIOGRAPHY.replace("# TECHNICAL BIOGRAPHY\n\n", "").split("\n\n"):
        story.append(Paragraph(p, styles['AcademicBody']))
        
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Generated PDF report with screenshots at: {output_path}")

if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "..", "Final_Project_Report.pdf")
    build_pdf_report(os.path.abspath(out_file))
