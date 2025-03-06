import openai
import asyncio
import logging
from config.settings import OPENAI_API_KEY, ASSISTANT_ID
from config.database import job_descriptions_collection, resumes_collection
from bson import ObjectId
from fastapi import HTTPException

# Initialize OpenAI Async Client
client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_resume(job_id: str, format: str = "pdf"):
    """Generates a tailored resume using OpenAI Assistant and stores it in MongoDB."""

    # 🔍 **Step 1: Fetch Job Data from MongoDB**
    job_entry = await job_descriptions_collection.find_one({"_id": ObjectId(job_id)})
    if not job_entry:
        raise HTTPException(status_code=404, detail="Job entry not found")

    job_data = job_entry.get("extracted_details", {})

    # 🛠 **Step 2: Ensure Required Fields**
    required_skills = job_data.get("required_skills", "General technical and industry-specific skills.")
    responsibilities = job_data.get("responsibilities", "Key job responsibilities will be tailored.")
    preferred_experience = job_data.get("preferred_experience", "Relevant industry experience will be highlighted.")

    # 📝 **Step 3: Optimized Prompt for OpenAI**
    job_prompt = f"""
    You are an **expert resume writer**. Generate a **high-quality, ATS-friendly resume** for **Timothy Riffe**, ensuring **PDF compatibility**.

    ### **Resume Format (Output must be plain text, NO Markdown!):**
    1. **Professional Summary** (3-4 concise sentences)
    2. **Key Skills** (List of expertise, formatted as "• Skill 1 • Skill 2 • Skill 3")
    3. **Work Experience** (Structured job roles)
    4. **Education & Certifications**
    5. **Technical Stack**
    6. **Military Service & Awards**

    ### **Strict Formatting Rules (IMPORTANT!):**
    - **NO Markdown symbols (#, *, -) in output.**  
    - **DO NOT include section headers in ALL CAPS.**  
    - **Ensure bullet points are properly formatted for PDF compatibility.**  
    - **NO extra formatting artifacts like "##", "**", or "_" should appear in the output.**  
    - **Use structured sections with clear spacing and indentation.**

    ### **Candidate Information:**
    - **Name:** Timothy Riffe
    - **Email:** timothy.riffe@unified-software-ai.com
    - **Phone:** (661) 809-6450
    - **LinkedIn:** linkedin.com/in/timothyriffe

    Return only the clean, well-structured resume in plain text format.
    """



    try:
        # 🔄 **Step 4: Create a Thread for OpenAI API**
        thread = await client.beta.threads.create()

        # 📝 **Step 5: Add the Prompt to the Thread**
        await client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=job_prompt
        )

        # 🚀 **Step 6: Run the Assistant**
        run = await client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # ⏳ **Step 7: Exponential Backoff Polling Mechanism**
        backoff = 2  # Start with a 2-second delay
        max_retries = 6  # Cap the retries at ~64 seconds max wait time

        for _ in range(max_retries):
            await asyncio.sleep(backoff)
            run_status = await client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

            if run_status.status not in ["queued", "in_progress"]:
                break  # Exit loop when processing is complete
            backoff *= 2  # Exponential increase in polling delay

        # 📥 **Step 8: Retrieve Generated Resume**
        messages = await client.beta.threads.messages.list(thread_id=thread.id)

        if messages.data and messages.data[0].content:
            generated_resume = messages.data[0].content[0].text.value.strip()
        else:
            logger.error("No resume generated from OpenAI")
            raise HTTPException(status_code=500, detail="Failed to generate resume")

        # 💾 **Step 9: Store Resume in MongoDB**
        resume_entry = {
            "job_id": job_id,
            "job_description": job_entry["job_description"],
            "extracted_details": job_data,
            "generated_resume": generated_resume
        }
        inserted_resume = await resumes_collection.insert_one(resume_entry)

        # 🔄 **Step 10: Update Job Entry with Resume**
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
        logger.error(f"OpenAI API Error: {e}")
        raise HTTPException(status_code=502, detail=f"OpenAI API Error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
