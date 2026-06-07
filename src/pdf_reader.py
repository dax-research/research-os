import os
import pdfplumber


def extract_text_from_pdf(pdf_path):

    pages = []

    with pdfplumber.open(pdf_path) as pdf:

        for page_number, page in enumerate(pdf.pages, start=1):

            page_text = page.extract_text()

            if page_text:
                pages.append({
                    "page_number": page_number,
                    "text": page_text
                })

    return {
        "filename": os.path.basename(pdf_path),
        "num_pages": len(pdf.pages),
        "pages": pages
    }