from fastapi import APIRouter

router = APIRouter(
    tags=["Health"],
)


@router.get("/")
def root():
    return {
        "project": "AI Resume Analyzer",
        "version": "1.0.0",
        "status": "running",
    }


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
    }