from app.config import settings
from app.utils.pdf import extract_text_from_pdf, pdf_to_images
from app.prompts.resume_prompt import build_resume_analysis_prompt
from app.services.groq_service import (
    generate_text_response,
    generate_vision_response,
)
from app.evaluators.ats_evaluator import calculate_ats_score


def format_ats_evaluation(evaluation: dict) -> str:
    skill_match = evaluation["skill_match"]

    return f"""
# Deterministic ATS Evaluation

## Calculated ATS Score
{evaluation["ats_score"]}/100

## Required Skills Found In JD
{", ".join(skill_match["required_skills"]) if skill_match["required_skills"] else "No known skills detected"}

## Matched Skills
{", ".join(skill_match["matched_skills"]) if skill_match["matched_skills"] else "No matched skills found"}

## Missing Skills
{", ".join(skill_match["missing_skills"]) if skill_match["missing_skills"] else "No missing skills found"}

## Skill Match Summary
Matched {skill_match["total_matched"]} out of {skill_match["total_required"]} required skills.
"""


def analyze_resume(
    resume_path: str,
    job_description: str,
) -> str:
    resume_text = extract_text_from_pdf(resume_path)

    if resume_text:
        evaluation = calculate_ats_score(
            resume_text=resume_text,
            job_description=job_description,
        )

        prompt = build_resume_analysis_prompt(
            resume_text=resume_text,
            job_description=job_description,
        )

        llm_result = generate_text_response(prompt)

        return format_ats_evaluation(evaluation) + "\n\n---\n\n" + llm_result

    prompt = build_resume_analysis_prompt(
        resume_text="Resume text not extracted. Analyze resume from attached images.",
        job_description=job_description,
    )

    image_output_dir = f"{settings.UPLOAD_DIR}/images"
    image_paths = pdf_to_images(
        file_path=resume_path,
        output_dir=image_output_dir,
    )

    return generate_vision_response(
        prompt=prompt,
        image_paths=image_paths[:2],
    )