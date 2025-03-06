import os
import chardet
import logging
import aiofiles
from fastapi import UploadFile
from pdfminer.high_level import extract_text
from docx import Document
from config.database import job_descriptions_collection

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

async def save_uploaded_file(file: UploadFile):
    """Saves uploaded job description file, extracts text, and stores it in MongoDB."""
    
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        # ✅ Save the file asynchronously
        async with aiofiles.open(file_path, "wb") as buffer:
            content = await file.read()
            await buffer.write(content)

        # ✅ Extract text using optimized function
        extracted_text = await extract_text_from_file(file_path, file.filename)
        if not extracted_text.strip():
            return {"error": "Failed to extract text from job description file"}

        # ✅ Store job description in MongoDB
        job_entry = {
            "job_description": extracted_text,
            "generated_resume": None
        }
        inserted_entry = await job_descriptions_collection.insert_one(job_entry)

        return {"job_id": str(inserted_entry.inserted_id), "extracted_text": extracted_text}

    except Exception as e:
        logging.error(f"❌ Error processing file: {e}")
        return {"error": str(e)}

async def extract_text_from_file(file_path: str, filename: str):
    """Extracts text from PDFs, DOCX, or TXT files asynchronously."""
    
    try:
        if filename.lower().endswith(".pdf"):
            return await extract_text_from_pdf(file_path)
        elif filename.lower().endswith(".docx"):
            return extract_text_from_docx(file_path)
        elif filename.lower().endswith(".txt"):
            return extract_text_from_txt(file_path)
        else:
            return None  # Unsupported format
    except Exception as e:
        logging.error(f"❌ Error extracting text: {e}")
        return None

async def extract_text_from_pdf(file_path: str):
    """Extracts text from a PDF file with optimized handling for large documents."""
    try:
        text = extract_text(file_path)
        return text.strip() if text else "No text extracted from PDF."
    except Exception as e:
        logging.error(f"❌ PDF extraction error: {e}")
        return None

def extract_text_from_docx(file_path: str):
    """Extracts text from a .docx file."""
    try:
        doc = Document(file_path)
        return "\n".join([para.text.strip() for para in doc.paragraphs if para.text.strip()])
    except Exception as e:
        logging.error(f"❌ DOCX extraction error: {e}")
        return None

def extract_text_from_txt(file_path: str):
    """Extracts text from a text file while handling encoding issues."""
    try:
        with open(file_path, "rb") as f:
            raw_data = f.read(10000)  # Read a portion of the file to detect encoding
            detected_encoding = chardet.detect(raw_data)["encoding"] or "utf-8"

        with open(file_path, "r", encoding=detected_encoding, errors="ignore") as f:
            return f.read().strip()
    except Exception as e:
        logging.error(f"❌ TXT extraction error: {e}")
        return None
