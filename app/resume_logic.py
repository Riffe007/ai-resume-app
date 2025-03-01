import openai
import asyncio
from config.settings import OPENAI_API_KEY, ASSISTANT_ID
from config.database import job_descriptions_collection, resumes_collection
from bson import ObjectId
from fastapi import HTTPException

# Initialize OpenAI Async Client
client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)

async def generate_resume(job_id: str, format: str = "pdf"):
    """Generates a tailored resume using OpenAI Assistants API and stores it in MongoDB."""

    # Fetch job description from MongoDB
    job_entry = await job_descriptions_collection.find_one({"_id": ObjectId(job_id)})
    if not job_entry:
        raise HTTPException(status_code=404, detail="Job entry not found")

    job_data = job_entry.get("extracted_details", {})

    # Ensure required fields exist, fallback to placeholders
    required_skills = job_data.get("required_skills", "N/A")
    responsibilities = job_data.get("responsibilities", "N/A")
    preferred_experience = job_data.get("preferred_experience", "N/A")

    # **Optimized Resume Prompt**
    job_prompt = f"""
    You are an **expert resume writer**. Your task is to generate a **high-quality, ATS-friendly resume** for **Timothy Riffe**.

    ### **Resume Requirements**
    - Use a **modern, structured format** optimized for **recruiters and ATS systems**.
    - Tailor the content to highlight **skills, responsibilities, and experience** from the job description.
    - **DO NOT include placeholders like "Not Specified".**
    - **Return ONLY the final resume in structured Markdown format.**

    ---

    📌 **Candidate Information:**
    - **Name:** Timothy Riffe
    - **Email:** timothy.riffe@example.com
    - **Phone:** (123) 456-7890
    - **LinkedIn:** linkedin.com/in/timothyriffe

    📌 **Professional Summary:**
    Write a **3-4 sentence summary** that showcases Timothy’s **top skills, leadership experience, and industry expertise**.

    📌 **Key Skills:**
    {required_skills if required_skills != "N/A" else "List 5-7 relevant technical and industry-specific skills."}

    📌 **Work Experience:**  
    Format each entry like this:

    🔹 **[Job Title]** — [Company Name]  
    📅 **[Start Date] – [End Date]**  
    📝 **Responsibilities & Achievements:**  
    - Use **bullet points** to show **measurable impact and results**.

    📌 **Education & Certifications:**  
    - List **degrees, certifications, and specialized training**.

    📌 **Technical Skills:**  
    - Mention **AI, ML, cybersecurity, cloud computing, and software engineering skills** relevant to Timothy's background.

    📌 **FORMAT:**
    - The resume should be written in **clean, professional Markdown**.
    - **Ensure ATS-friendliness** by structuring bullet points and experience effectively.
    - Make the output look **exactly like a professional resume**.

    **Return only the final resume. Do NOT include this instruction text.**
    """

    try:
        # **Step 1: Create a Thread**
        thread = await client.beta.threads.create()

        # **Step 2: Add the user's message to the Thread**
        await client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=job_prompt
        )

        # **Step 3: Run the Assistant on the Thread**
        run = await client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # **Step 4: Poll for Completion**
        while True:
            await asyncio.sleep(2)  # Small delay to prevent excessive polling
            run_status = await client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status not in ["queued", "in_progress"]:
                break  # Exit loop when processing is complete

        # **Step 5: Retrieve Messages from the Thread**
        messages = await client.beta.threads.messages.list(thread_id=thread.id)

        # **Extract Generated Resume**
        if messages.data and messages.data[0].content:
            generated_resume = messages.data[0].content[0].text.value.strip()
        else:
            raise HTTPException(status_code=500, detail="No resume generated from OpenAI")

        # **Step 6: Store Resume in MongoDB**
        resume_entry = {
            "job_id": job_id,
            "job_description": job_entry["job_description"],
            "extracted_details": job_data,
            "generated_resume": generated_resume
        }
        inserted_resume = await resumes_collection.insert_one(resume_entry)

        # **Step 7: Update Job Entry with Resume**
        await job_descriptions_collection.update_one(
            {"_id": ObjectId(job_id)},
            {"$set": {"generated_resume": generated_resume}}
        )

        return {
            "message": "✅ Resume generated successfully!",
            "resume_id": str(inserted_resume.inserted_id),
            "generated_resume": generated_resume
        }

    except openai.APIError as e:
        raise HTTPException(status_code=502, detail=f"OpenAI API Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
