import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")  # ✅ Corrected variable name

# MongoDB Connection URI
MONGO_URI = os.getenv("MONGO_URI")

# Ensure values are loaded
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY is not set in .env")

if not ASSISTANT_ID:
    raise ValueError("❌ ASSISTANT_ID is not set in .env")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI is not set in .env")

print(f"✅ Environment variables loaded: ASSISTANT_ID={ASSISTANT_ID}")
