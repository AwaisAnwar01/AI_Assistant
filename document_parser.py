# app/document_parser.py

from pdfminer.high_level import extract_text

def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file.
    :param file_path: Path to the PDF file.
    :return: Extracted text as a string.
    """
    text = extract_text(file_path)
    return text
