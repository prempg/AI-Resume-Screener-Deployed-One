from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.resume import router as resume_router

app = FastAPI(
    title="AI Resume Analyzer API",
    version="1.0.0",
    description="Analyze resumes against job descriptions using AI.",
)

app.include_router(health_router)
app.include_router(resume_router)
