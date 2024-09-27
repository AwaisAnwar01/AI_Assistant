from pdfminer.high_level import extract_text
import docx
import pandas as pd
import os
from PIL import Image
import pytesseract

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    text = extract_text(file_path)
    return text

def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_txt(file_path):
    """Extract text from a TXT file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text_from_csv(file_path):
    """Extract text from a CSV file."""
    df = pd.read_csv(file_path)
    return df.to_string()

def extract_text_from_image(file_path):
    """Extract text from an image file using OCR."""
    try:
        img = Image.open(file_path)

        # Check if the image is in a valid format
        img = img.convert('RGB')  # Convert to RGB if it's not
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        raise ValueError(f"Error processing the image: {e}")


def parse_document(file_path):
    """Determine the file type and extract text accordingly."""
    file_extension = os.path.splitext(file_path)[-1].lower()

    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_path)
    elif file_extension == '.txt':
        return extract_text_from_txt(file_path)
    elif file_extension == '.csv':
        return extract_text_from_csv(file_path)
    elif file_extension in ['.jpg', '.jpeg', '.png']:  # Add more image formats if needed
        return extract_text_from_image(file_path)
    else:
        raise ValueError("Unsupported file format: {}".format(file_extension))
