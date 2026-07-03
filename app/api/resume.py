from fastapi import APIRouter, UploadFile, Form, Path
from bson import ObjectId

from app.utils.file import save_to_disk
from app.utils.pdf import extract_jd_text
from app.db.collections.files import files_collection
from app.job_queue.q import q
from app.job_queue.workers import process_resume_analysis

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


@router.post("/analyze")
async def analyze_resume_api(
    resume_pdf: UploadFile,
    job_description_text: str | None = Form(None),
    jd_pdf: UploadFile | None = None,
):
    jd_pdf_path = None

    if jd_pdf:
        jd_pdf_path = f"/mnt/uploads/jd/{jd_pdf.filename}"
        await save_to_disk(
            file=await jd_pdf.read(),
            path=jd_pdf_path,
        )

    final_job_description = extract_jd_text(
        jd_text=job_description_text,
        jd_pdf_path=jd_pdf_path,
    )

    db_file = await files_collection.insert_one(
        {
            "name": resume_pdf.filename,
            "status": "saving",
            "result": None,
            "job_description": final_job_description,
            "file_type": "resume_analysis",
        }
    )

    file_path = f"/mnt/uploads/{str(db_file.inserted_id)}/{resume_pdf.filename}"

    await save_to_disk(
        file=await resume_pdf.read(),
        path=file_path,
    )

    q.enqueue(
        process_resume_analysis,
        str(db_file.inserted_id),
        file_path,
        final_job_description,
    )

    await files_collection.update_one(
        {"_id": db_file.inserted_id},
        {"$set": {"status": "queued"}},
    )

    return {
        "file_id": str(db_file.inserted_id),
        "status": "queued",
    }


@router.get("/{file_id}")
async def get_resume_analysis_result(
    file_id: str = Path(..., description="Resume analysis file ID"),
):
    db_file = await files_collection.find_one(
        {"_id": ObjectId(file_id)}
    )

    if not db_file:
        return {
            "error": "File not found"
        }

    return {
        "file_id": str(db_file["_id"]),
        "name": db_file.get("name"),
        "status": db_file.get("status"),
        "file_type": db_file.get("file_type"),
        "job_description": db_file.get("job_description"),
        "result": db_file.get("result"),
    }