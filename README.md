# AI Resume Generator

## 🚀 Overview
AI-powered resume generation app that extracts job descriptions, analyzes key skills, and generates a tailored, ATS-friendly resume for **Timothy Riffe**. Uses **FastAPI**, **MongoDB**, and **OpenAI Assistants API** for intelligent resume creation.

---

## 📌 Features
✅ Upload job descriptions in **PDF, DOCX, or TXT** format  
✅ Extract and analyze **key skills, responsibilities, and experience**  
✅ Generate **high-quality, ATS-optimized resumes**  
✅ Store and retrieve resumes from **MongoDB**  
✅ Uses **OpenAI Assistants API** for resume writing  
✅ Supports **JSON-based API calls for automation**  

---

## ⚡ Tech Stack
- **Backend:** FastAPI, Python 3.x
- **AI Integration:** OpenAI Assistants API
- **Database:** MongoDB (via Motor for async support)
- **File Handling:** pdfminer, python-docx
- **Deployment:** Uvicorn, Docker (optional)

---

## 🔧 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/ai-resume-app.git
cd ai-resume-app
```
## 2️⃣ Set Up Virtual Environment
```bash
python -m venv resume-env
source resume-env/bin/activate  # macOS/Linux
resume-env\Scripts\activate  # Windows
```
## 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
## 4️⃣ Configure Environment Variables
Create a .env file in the root directory and add your credentials:
```plaintext
MONGO_URI=your_mongodb_connection_string
OPENAI_API_KEY=your_openai_api_key
ASSISTANT_ID=your_openai_assistant_id
```
## 5️⃣ Run the Application
```bash
uvicorn app.main:app --reload
```
# 📡 API Endpoints
### 🔹 Upload Job Description
```http
POST /upload_job_description?format=pdf
```
### Payload (multipart/form-data)
- file: PDF, DOCX, or TXT file
### Response
```json
{
  "message": "Resume generated successfully!",
  "resume": {
    "resume_id": "67c254645e2ee7ea4ac5c73b",
    "generated_resume": "AI-generated resume text here..."
  }
}
```
### 🔹 Retrieve a Resume
```http
GET /resume/{resume_id}
```
### 🔹 List All Resumes
```http
GET /resumes
```

# 🛠 Troubleshooting
- MongoDB Connection Error? Ensure MongoDB is running and MONGO_URI is correct.
- API Key Issues? Ensure the - OPENAI_API_KEY is valid.
- Push to GitHub Fails? Ensure .gitignore includes .env and clear cache:
```bash 
git rm --cached .env
git commit -m "Removed .env from repo"
```

# 🤝 Contributing
Want to improve the AI Resume Generator? Follow these steps:

1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Push to your fork
5. Open a PR 🚀

# 📜 License
This project is MIT Licensed.
