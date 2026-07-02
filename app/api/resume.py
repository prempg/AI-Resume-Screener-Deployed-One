from fastapi import APIRouter, UploadFile, Form
from fastapi import Path
from bson import ObjectId
from app.utils.file import save_to_disk
from app.db.collections.files import files_collection
from app.queue.q import q
from app.queue.workers import process_resume_analysis

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


@router.post("/analyze")
async def analyze_resume_api(
    resume_pdf: UploadFile,
    job_description_text: str = Form(...),
):
    db_file = await files_collection.insert_one(
        {
            "name": resume_pdf.filename,
            "status": "saving",
            "result": None,
            "job_description": job_description_text,
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
        job_description_text,
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