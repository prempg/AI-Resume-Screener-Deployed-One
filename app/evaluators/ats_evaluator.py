import re


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_required_skills(job_description: str) -> list[str]:
    known_skills = [
        "python",
        "java",
        "node.js",
        "javascript",
        "typescript",
        "fastapi",
        "django",
        "flask",
        "sql",
        "mongodb",
        "redis",
        "docker",
        "kubernetes",
        "aws",
        "gcp",
        "azure",
        "sagemaker",
        "vertex ai",
        "azure ml",
        "mlflow",
        "kubeflow",
        "langchain",
        "langgraph",
        "llm",
        "llms",
        "rag",
        "transformers",
        "hugging face",
        "embedding",
        "embeddings",
        "vector database",
        "qdrant",
        "pinecone",
        "weaviate",
        "chroma",
        "faiss",
        "mistral",
        "llama",
        "gpt",
        "claude",
        "prompt engineering",
        "prompt tuning",
        "mlops",
        "etl",
        "data pipeline",
        "data engineering",
        "pandas",
        "numpy",
        "scikit-learn",
        "machine learning",
        "deep learning",
        "nlp",
    ]

    jd = normalize_text(job_description)

    required_skills = []

    for skill in known_skills:
        if skill in jd:
            required_skills.append(skill)

    return sorted(set(required_skills))


def calculate_skill_match(
    resume_text: str,
    job_description: str,
) -> dict:
    resume = normalize_text(resume_text)
    required_skills = extract_required_skills(job_description)

    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill in resume:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    total_required = len(required_skills)
    total_matched = len(matched_skills)

    if total_required == 0:
        score = 0
    else:
        score = round((total_matched / total_required) * 100, 2)

    return {
        "score": score,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_required": total_required,
        "total_matched": total_matched,
    }


def calculate_ats_score(
    resume_text: str,
    job_description: str,
) -> dict:
    skill_result = calculate_skill_match(
        resume_text=resume_text,
        job_description=job_description,
    )

    final_score = skill_result["score"]

    return {
        "ats_score": final_score,
        "skill_match": skill_result,
    }