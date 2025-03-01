import os
import chardet
import re
import logging
from fastapi import UploadFile
from pdfminer.high_level import extract_text
from docx import Document
from config.database import job_descriptions_collection

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define Upload Directory
UPLOAD_FOLDER = "uploads"

async def save_uploaded_file(file: UploadFile):
    """Saves an uploaded job description file, extracts text, and stores it in MongoDB."""

    try:
        # Ensure the uploads directory exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Define file path
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Extract text based on file type
        extracted_text = await extract_text_from_file(file_path, file.filename)

        if not extracted_text:
            logging.error("Failed to extract text from the file.")
            return {"error": "Unsupported file format or failed to extract text"}

        # Extract job details from the text
        job_data = extract_job_details(extracted_text)

        # Store job description in MongoDB
        job_entry = {
            "job_description": extracted_text,
            "extracted_details": job_data,
            "generated_resume": None,  # Resume will be added later
            "file_path": file_path
        }

        # ✅ Await MongoDB insert operation
        inserted_entry = await job_descriptions_collection.insert_one(job_entry)

        return {
            "file_path": file_path,
            "job_data": job_data,
            "job_id": str(inserted_entry.inserted_id) if inserted_entry else None
        }

    except Exception as e:
        logging.error(f"Error processing uploaded file: {e}")
        return {"error": f"Unexpected error occurred: {str(e)}"}


async def extract_text_from_file(file_path: str, filename: str):
    """Extracts text from PDFs, DOCX, or TXT files asynchronously."""
    try:
        if filename.lower().endswith(".pdf"):
            return await extract_text_from_pdf(file_path)  # Extract text from PDF
        elif filename.lower().endswith(".docx"):
            return extract_text_from_docx(file_path)  # Extract text from DOCX
        elif filename.lower().endswith(".txt"):
            return extract_text_from_txt(file_path)  # Extract text from TXT
        else:
            return None  # Unsupported file format
    except Exception as e:
        logging.error(f"Error extracting text: {e}")
        return None


async def extract_text_from_pdf(file_path: str):
    """Asynchronously extracts text from a PDF file."""
    try:
        return extract_text(file_path).strip()
    except Exception as e:
        logging.error(f"Error extracting PDF text: {e}")
        return None


def extract_text_from_docx(file_path: str):
    """Extracts text from a .docx file."""
    try:
        doc = Document(file_path)
        return "\n".join([para.text.strip() for para in doc.paragraphs if para.text.strip()])
    except Exception as e:
        logging.error(f"Error extracting DOCX text: {e}")
        return None


def extract_text_from_txt(file_path: str):
    """Extracts text from a text file while handling encoding issues."""
    try:
        with open(file_path, "rb") as f:
            raw_data = f.read(10000)  # Read a portion of the file
            detected_encoding = chardet.detect(raw_data)["encoding"] or "utf-8"

        with open(file_path, "r", encoding=detected_encoding, errors="ignore") as f:
            return f.read().strip()
    except Exception as e:
        logging.error(f"Error extracting TXT text: {e}")
        return None


def extract_job_details(content: str):
    """Extracts key job requirements from the job description text."""
    try:
        required_skills = re.findall(r"(?:Required Skills|Key Skills):\s*(.*)", content, re.IGNORECASE)
        responsibilities = re.findall(r"(?:Responsibilities|Duties):\s*(.*)", content, re.IGNORECASE)
        preferred_experience = re.findall(r"(?:Preferred Experience|Qualifications):\s*(.*)", content, re.IGNORECASE)

        return {
            "required_skills": required_skills[0] if required_skills else "Not specified",
            "responsibilities": responsibilities[0] if responsibilities else "Not specified",
            "preferred_experience": preferred_experience[0] if preferred_experience else "Not specified"
        }
    except Exception as e:
        logging.error(f"Error extracting job details: {e}")
        return {"error": f"Failed to extract job details: {str(e)}"}
