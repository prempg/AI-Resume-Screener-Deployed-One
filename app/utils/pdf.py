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

def extract_jd_text(
    jd_text: str | None = None,
    jd_pdf_path: str | None = None,
) -> str:
    if jd_text and jd_text.strip():
        return jd_text.strip()

    if jd_pdf_path:
        extracted_text = extract_text_from_pdf(jd_pdf_path)

        if extracted_text:
            return extracted_text

        raise ValueError(
            "Could not extract text from JD PDF. "
            "Please paste the Job Description as text."
        )

    raise ValueError(
        "Please provide either JD text or JD PDF."
    )
