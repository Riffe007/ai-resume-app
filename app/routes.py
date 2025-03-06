import logging
import asyncio
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.file_uploads import save_uploaded_file
from app.resume_logic import generate_resume
from app.generate_pdf import generate_pdf_resume
from config.database import resumes_collection
from bson import ObjectId

# ✅ Set up Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Declare FastAPI Router
router = APIRouter()


@router.post("/upload")
async def upload_file_and_generate_resume(file: UploadFile = File(...)):
    """
    🚀 Handles file upload, extracts job description, generates a resume, and returns a **pristine** PDF ready for download.
    """

    try:
        # ✅ **Step 1: Save & Extract Job Description**
        file_data = await save_uploaded_file(file)
        if "error" in file_data:
            logger.error(f"File processing error: {file_data['error']}")
            raise HTTPException(status_code=400, detail=file_data["error"])

        job_id = file_data["job_id"]
        logger.info(f"✅ Job description extracted successfully! Job ID: {job_id}")

        # ✅ **Step 2: Parallel Resume Generation & PDF Conversion**
        resume_data = await generate_resume(job_id)

        if not resume_data.get("generated_resume"):
            logger.error("❌ Resume generation failed.")
            raise HTTPException(status_code=500, detail="Resume generation failed.")

        markdown_resume = resume_data["generated_resume"]
        resume_id = resume_data["resume_id"]
        logger.info(f"✅ AI-generated resume stored in MongoDB. Resume ID: {resume_id}")

        # ✅ **Step 3: Convert Resume to PDF in Parallel**
        pdf_path = await asyncio.to_thread(generate_pdf_resume, markdown_resume, resume_id)

        if not os.path.exists(pdf_path):
            logger.error(f"❌ PDF generation failed. Path does not exist: {pdf_path}")
            raise HTTPException(status_code=500, detail="Failed to generate resume PDF.")

        logger.info(f"✅ PDF resume successfully generated at: {pdf_path}")

        # ✅ **Step 4: Store PDF Path in Database**
        update_result = await resumes_collection.update_one(
            {"_id": ObjectId(resume_id)}, {"$set": {"pdf_path": pdf_path}}
        )

        if update_result.modified_count == 0:
            logger.warning("⚠️ Database update failed: PDF path not saved.")
            raise HTTPException(status_code=500, detail="Failed to save PDF resume path.")

        # ✅ **Step 5: Auto-download PDF (UI Calls This Directly)**
        return FileResponse(
            path=pdf_path,
            filename="Timothy_Riffe_Resume.pdf",
            media_type="application/pdf",
        )

    except Exception as e:
        logger.error(f"🔥 Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the resume.")


@router.get("/download/{resume_id}")
async def download_resume(resume_id: str):
    """
    🎯 Fetches a generated resume and returns it as a downloadable **pristine PDF**.
    """

    try:
        # ✅ **Step 1: Check Database for Resume**
        resume_data = await resumes_collection.find_one({"_id": ObjectId(resume_id)})
        if not resume_data:
            raise HTTPException(status_code=404, detail="Resume not found in database.")

        # ✅ **Step 2: Verify the PDF Path Exists**
        pdf_path = os.path.join("generated_pdfs", f"resume_{resume_id}.pdf")

        if not os.path.exists(pdf_path):
            logger.error(f"❌ Resume PDF file missing: {pdf_path}")
            raise HTTPException(status_code=404, detail="Resume PDF not found.")

        # ✅ **Step 3: Serve the PDF File for Download**
        return FileResponse(
            path=pdf_path,
            filename="Timothy_Riffe_Resume.pdf",
            media_type="application/pdf",
        )

    except Exception as e:
        logger.error(f"🔥 Error while fetching resume PDF: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve resume PDF.")
