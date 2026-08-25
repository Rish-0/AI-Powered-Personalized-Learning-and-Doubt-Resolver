import fitz

from pathlib import Path

from app.services.parser.cleaner import TextCleaner


class PDFParser:

    def extract_text(self, pdf_path: str):

        document = fitz.open(pdf_path)

        pages = []

        for page_number in range(len(document)):

            page = document.load_page(page_number)

            raw_text = page.get_text()

            clean_text = TextCleaner.clean(raw_text)

            pages.append({

                "page": page_number + 1,

                "source": Path(pdf_path).name,

                "text": clean_text

            })

        document.close()

        return pages