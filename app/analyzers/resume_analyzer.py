from app.config import settings
from app.utils.pdf import extract_text_from_pdf, pdf_to_images
from app.prompts.resume_prompt import build_resume_analysis_prompt
from app.services.groq_service import (
    generate_text_response,
    generate_vision_response,
)


def analyze_resume(
    resume_path: str,
    job_description: str,
) -> str:
    resume_text = extract_text_from_pdf(resume_path)

    prompt = build_resume_analysis_prompt(
        #flake8: noqa
        resume_text=resume_text if resume_text else "Resume text not extracted. Analyze resume from attached images.",
        job_description=job_description,
    )

    if resume_text:
        return generate_text_response(prompt)

    image_output_dir = f"{settings.UPLOAD_DIR}/images"
    image_paths = pdf_to_images(
        file_path=resume_path,
        output_dir=image_output_dir,
    )

    return generate_vision_response(
        prompt=prompt,
        image_paths=image_paths[:2],
    )
