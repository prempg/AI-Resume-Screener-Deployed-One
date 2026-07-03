from bson import ObjectId

from app.db.collections.files import files_collection
from app.analyzers.resume_analyzer import analyze_resume_with_metadata


async def process_resume_analysis(
    id: str,
    resume_path: str,
    job_description: str,
):
    await files_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "processing"}},
    )

    try:
        analysis_data = analyze_resume_with_metadata(
            resume_path=resume_path,
            job_description=job_description,
        )

        await files_collection.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "status": "processed",
                    "result": analysis_data["report"],
                    "ats_score": analysis_data["ats_score"],
                    "matched_skills": analysis_data["matched_skills"],
                    "missing_skills": analysis_data["missing_skills"],
                    "required_skills": analysis_data["required_skills"],
                    "used_vision_fallback": analysis_data["used_vision_fallback"],
                }
            },
        )

    except Exception as e:
        await files_collection.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "status": "failed",
                    "result": str(e),
                }
            },
        )