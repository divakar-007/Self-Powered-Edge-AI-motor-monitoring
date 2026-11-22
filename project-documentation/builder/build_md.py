# -*- coding: utf-8 -*-
"""
build_md.py - Assembles master Markdown report Project_Report_Source.md
"""

import os
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

def format_markdown_table(table_dict):
    headers = table_dict["headers"]
    rows = table_dict["rows"]
    md = f"### {table_dict['title']}\n\n"
    md += "| " + " | ".join(headers) + " |\n"
    md += "| " + " | ".join([":---"] * len(headers)) + " |\n"
    for row in rows:
        md += "| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |\n"
    md += "\n"
    return md

def generate_markdown(output_path):
    md = []
    
    # Title Page
    md.append(f"# {TITLE}\n")
    md.append(f"**A PROJECT REPORT**\n")
    md.append(f"*Submitted in partial fulfillment of the requirements for the award of the degree of*\n")
    md.append(f"### {DEGREE} IN {BRANCH}\n")
    md.append(f"**Submitted by:**\n")
    md.append(f"**{PLACEHOLDERS['STUDENT_NAME']}** (Reg. No: **{PLACEHOLDERS['REG_NO']}**)\n")
    md.append(f"**Under the Guidance of:**\n")
    md.append(f"**{PLACEHOLDERS['GUIDE_NAME']}**, {PLACEHOLDERS['GUIDE_DESIGNATION']}\n")
    md.append(f"**{PLACEHOLDERS['DEPARTMENT']}**  \n")
    md.append(f"**{PLACEHOLDERS['COLLEGE_NAME']}**, {PLACEHOLDERS['COLLEGE_ADDRESS']}  \n")
    md.append(f"**Affiliated to {PLACEHOLDERS['UNIVERSITY']}**  \n")
    md.append(f"**Academic Year: {PLACEHOLDERS['ACADEMIC_YEAR']}**\n\n---\n")
    
    # Certificate
    md.append(f"# CERTIFICATE\n\n{CERTIFICATE_TEXT}\n\n")
    md.append(f"**{PLACEHOLDERS['GUIDE_NAME']}**  \nProject Guide  \n\n")
    md.append(f"**{PLACEHOLDERS['HOD_NAME']}**  \nHead of the Department  \n\n---\n")
    
    # Declaration
    md.append(f"# DECLARATION\n\n{DECLARATION_TEXT}\n\n")
    md.append(f"Place: _______________  \nDate: _______________  \n\n**{PLACEHOLDERS['STUDENT_NAME']}**  \n\n---\n")
    
    # Acknowledgement
    md.append(f"# ACKNOWLEDGEMENT\n\n{ACKNOWLEDGEMENT_TEXT}\n\n---\n")
    
    # Abstract
    md.append(f"# ABSTRACT\n\n{ABSTRACT_TEXT}\n\n---\n")
    
    # Table of Contents
    md.append("# TABLE OF CONTENTS\n")
    md.append("- **Front Matter**\n")
    md.append("  - Certificate\n  - Declaration\n  - Acknowledgement\n  - Abstract\n  - Table of Contents\n  - List of Figures\n  - List of Tables\n  - List of Abbreviations\n")
    md.append("- **Chapter 1: Introduction**\n")
    for s in CH1_SECTIONS:
        md.append(f"  - {s['number']} {s['title']}\n")
    md.append("- **Chapter 2: Literature Survey**\n")
    for s in CH2_SECTIONS:
        md.append(f"  - {s['number']} {s['title']}\n")
    md.append("- **Chapter 3: Problem Definition and Methodology**\n")
    for s in CH3_SECTIONS:
        md.append(f"  - {s['number']} {s['title']}\n")
    md.append("- **Chapter 4: Design Overview**\n")
    for s in CH4_SECTIONS:
        md.append(f"  - {s['number']} {s['title']}\n")
    md.append("- **Chapter 5: Implementation**\n")
    for s in CH5_SECTIONS:
        md.append(f"  - {s['number']} {s['title']}\n")
    md.append("- **Chapter 6: Results and Discussion**\n")
    for s in CH6_SECTIONS:
        md.append(f"  - {s['number']} {s['title']}\n")
    md.append("- **Chapter 7: Conclusion and Future Scope**\n")
    for s in CH7_SECTIONS:
        md.append(f"  - {s['number']} {s['title']}\n")
    md.append("- **References**\n")
    md.append("- **Appendices (A1 - A8)**\n")
    md.append("- **Technical Biography**\n\n---\n")
    
    # Chapters
    # Chapter 1
    md.append(f"# {CHAPTER_1_TITLE}\n\n")
    for s in CH1_SECTIONS:
        md.append(f"## {s['number']} {s['title']}\n\n{s['content']}\n\n")
    md.append("---\n")
    
    # Chapter 2
    md.append(f"# {CHAPTER_2_TITLE}\n\n")
    for s in CH2_SECTIONS:
        md.append(f"## {s['number']} {s['title']}\n\n{s['content']}\n\n")
    md.append(format_markdown_table(TABLE_2_1_DATA))
    md.append("---\n")
    
    # Chapter 3
    md.append(f"# {CHAPTER_3_TITLE}\n\n")
    for s in CH3_SECTIONS:
        md.append(f"## {s['number']} {s['title']}\n\n{s['content']}\n\n")
    md.append("---\n")
    
    # Chapter 4
    md.append(f"# {CHAPTER_4_TITLE}\n\n")
    for s in CH4_SECTIONS:
        md.append(f"## {s['number']} {s['title']}\n\n{s['content']}\n\n")
    md.append(format_markdown_table(TABLE_4_1_DATA))
    md.append("---\n")
    
    # Chapter 5
    md.append(f"# {CHAPTER_5_TITLE}\n\n")
    for s in CH5_SECTIONS:
        md.append(f"## {s['number']} {s['title']}\n\n{s['content']}\n\n")
    md.append("---\n")
    
    # Chapter 6
    md.append(f"# {CHAPTER_6_TITLE}\n\n")
    for s in CH6_SECTIONS:
        md.append(f"## {s['number']} {s['title']}\n\n{s['content']}\n\n")
    md.append(format_markdown_table(TABLE_6_1_DATA))
    md.append(format_markdown_table(TABLE_6_2_DATA))
    md.append(format_markdown_table(TABLE_6_3_DATA))
    md.append(format_markdown_table(TABLE_6_4_DATA))
    md.append(format_markdown_table(TABLE_6_5_DATA))
    md.append(format_markdown_table(TABLE_6_6_DATA))
    md.append("---\n")
    
    # Chapter 7
    md.append(f"# {CHAPTER_7_TITLE}\n\n")
    for s in CH7_SECTIONS:
        md.append(f"## {s['number']} {s['title']}\n\n{s['content']}\n\n")
    md.append("---\n")
    
    # References
    md.append("# REFERENCES\n\n")
    for ref in REFERENCES_LIST:
        md.append(f"{ref}\n\n")
    md.append("---\n")
    
    # Appendices
    for app in [APPENDIX_A1, APPENDIX_A2, APPENDIX_A3, APPENDIX_A4, APPENDIX_A5, APPENDIX_A6, APPENDIX_A7, APPENDIX_A8]:
        md.append(f"# {app['title']}\n\n```\n{app['content']}\n```\n\n---\n")
        
    # Technical Biography
    md.append(f"{TECHNICAL_BIOGRAPHY}\n")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("".join(md))
    print(f"[SUCCESS] Generated Markdown report at: {output_path}")

if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "..", "Project_Report_Source.md")
    generate_markdown(os.path.abspath(out_file))
