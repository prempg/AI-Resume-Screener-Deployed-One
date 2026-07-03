import os
from pdf2image import convert_from_path
import fitz


def extract_text_from_pdf(file_path: str) -> str:
    text = ""

    with fitz.open(file_path) as pdf:
        print("Pages:", len(pdf))

        for page_number, page in enumerate(pdf):
            page_text = page.get_text()

            print(
                f"Page {page_number + 1}:",
                len(page_text)
            )

            text += page_text

    return text.strip()


def pdf_to_images(file_path: str, output_dir: str) -> list[str]:
    pages = convert_from_path(file_path)
    images = []

    os.makedirs(output_dir, exist_ok=True)

    for i, page in enumerate(pages):
        image_path = os.path.join(output_dir, f"image-{i}.jpg")
        page.save(image_path, "JPEG")
        images.append(image_path)

    return images
