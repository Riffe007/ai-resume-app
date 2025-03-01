from fastapi import APIRouter, UploadFile, File
from app.resume_logic import generate_resume
from app.file_uploads import save_uploaded_file
from config.database import job_descriptions_collection

router = APIRouter()

@router.post("/upload_job_description")
async def upload_file_and_generate_resume(file: UploadFile = File(...), format: str = "pdf"):
    """Handles file upload, extracts job description, and generates a resume."""

    # Save and extract text from the file
    file_data = await save_uploaded_file(file)

    if "error" in file_data:
        return file_data  # Return error if extraction failed

    job_id = file_data["job_id"]

    # Generate resume
    resume = await generate_resume(job_id, format)

    return {"message": "Resume generated successfully!", "resume": resume}
