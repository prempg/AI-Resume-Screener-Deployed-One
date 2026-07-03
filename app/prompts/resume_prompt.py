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
def build_resume_text_extraction_prompt() -> str:
    return """
Extract all readable text from this resume image.

Rules:
- Return only the extracted resume text.
- Do not analyze the resume.
- Do not add suggestions.
- Preserve sections like Education, Skills, Projects, Experience.
- If some text is unclear, write [unclear].
"""