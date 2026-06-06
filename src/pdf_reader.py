import os
import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        num_pages = len(pdf.pages)

        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return {
        "filename": os.path.basename(pdf_path),
        "num_pages": num_pages,
        "text": text
    }