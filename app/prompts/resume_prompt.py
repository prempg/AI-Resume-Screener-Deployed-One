def build_resume_analysis_prompt(
    resume_text: str,
    job_description: str,
) -> str:
    return f"""
You are an expert ATS resume reviewer and technical recruiter.

Analyze the candidate resume according to the given job description.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Return the answer in this exact format:

# Resume Analysis Report

## ATS Match Score
Give score out of 100 with a short reason.

## Strong Points
Mention resume strengths according to the JD.

## Weak Points
Mention resume weaknesses according to the JD.

## Missing Skills
List important skills missing from resume.

## Improvement Suggestions
Give practical resume improvements.

## Better Resume Bullet Points
Rewrite 5 strong resume bullet points.

## Final Advice
Give clear next steps.

Keep it honest, helpful, and beginner-friendly.
"""
