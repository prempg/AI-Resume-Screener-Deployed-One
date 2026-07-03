from app.config import settings
from app.utils.pdf import extract_text_from_pdf, pdf_to_images
from app.prompts.resume_prompt import (
    build_resume_analysis_prompt,
    build_resume_text_extraction_prompt,
)
from app.services.groq_service import (
    generate_text_response,
    generate_vision_response,
    extract_text_from_images,
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

    image_output_dir = f"{settings.UPLOAD_DIR}/images"
    image_paths = pdf_to_images(
        file_path=resume_path,
        output_dir=image_output_dir,
    )

    extraction_prompt = build_resume_text_extraction_prompt()

    extracted_resume_text = extract_text_from_images(
        prompt=extraction_prompt,
        image_paths=image_paths[:2],
    )

    evaluation = calculate_ats_score(
        resume_text=extracted_resume_text,
        job_description=job_description,
    )

    analysis_prompt = build_resume_analysis_prompt(
        resume_text=extracted_resume_text,
        job_description=job_description,
    )

    llm_result = generate_vision_response(
        prompt=analysis_prompt,
        image_paths=image_paths[:2],
    )

    return format_ats_evaluation(evaluation) + "\n\n---\n\n" + llm_result
