from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

OUTPUT_PATH = "testingFolder/output.docx"

def contains_chinese(char):
    """Check if a character is Chinese"""
    return '\u4e00' <= char <= '\u9fff'

def text_to_word(text: str, output_path: str = OUTPUT_PATH):
    """
    Convert a string to a Word (.docx) file with mixed font handling.
    Chinese characters use a specific font, English letters use another font and can be italic.

    :param text: input string
    :param output_path: output file path, e.g., "output.docx"
    """
    doc = Document()
    
    # Split text by line to preserve line breaks
    for line in text.split("\n"):
        p = doc.add_paragraph()
        for char in line:
            run = p.add_run(char)
            
            if contains_chinese(char):
                # Chinese font
                run.font.name = "標楷體"
                run._element.rPr.rFonts.set(qn("w:eastAsia"), "標楷體")
            else:
                # English font
                run.font.name = "Times New Roman"
                run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
                if char.isalpha():
                    run.italic = True
            
            run.font.size = Pt(12)
    
    doc.save(output_path)
    return