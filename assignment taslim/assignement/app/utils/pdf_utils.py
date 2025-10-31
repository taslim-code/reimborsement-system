# PDF parsing utilities
import PyPDF2
from typing import BinaryIO

def extract_text_from_pdf(pdf_file: BinaryIO) -> str:
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
