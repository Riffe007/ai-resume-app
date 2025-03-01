from motor.motor_asyncio import AsyncIOMotorClient  # Use async MongoDB client
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Retrieve the MongoDB URI
MONGO_URI = os.getenv("MONGO_URI")

# Ensure MONGO_URI is set
if not MONGO_URI:
    raise ValueError("❌ MONGO_URI is not set in .env")

# Connect to MongoDB (Async)
client = AsyncIOMotorClient(MONGO_URI)
db = client["resume_ai"]  # Database name

# Collections (Async)
job_descriptions_collection = db["job_descriptions"]
resumes_collection = db["resumes"]

print("✅ Connected to MongoDB asynchronously using Motor!")
