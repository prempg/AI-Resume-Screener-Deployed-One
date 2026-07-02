from app.utils.pdf import extract_text_from_pdf
from app.prompts.resume_prompt import build_resume_analysis_prompt
from app.services.groq_service import generate_text_response


def analyze_resume(
    resume_path: str,
    job_description: str,
) -> str:
    """
    Analyze a resume against a job description.
    """

    resume_text = extract_text_from_pdf(resume_path)

    if not resume_text:
        raise ValueError(
            "Could not extract text from resume."
        )

    prompt = build_resume_analysis_prompt(
        resume_text=resume_text,
        job_description=job_description,
    )

    result = generate_text_response(prompt)

    return result
