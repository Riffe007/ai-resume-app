import logging
import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from app.routes import router  # ✅ Ensure correct import

# ✅ Load Environment Variables
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://interactive-resume-brown.vercel.app")  # Default to Vercel URL
PORT = int(os.getenv("PORT", 8000))

# ✅ Set up Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ✅ Initialize FastAPI App with Metadata
app = FastAPI(
    title="Timothy Riffe Resume AI",
    description="AI-driven resume generation and PDF conversion API.",
    version="1.0.0"
)

# ✅ Enable CORS for Frontend (Supports both Production & Local Development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:3000"],  # Vercel + Local Dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include Routes
app.include_router(router)

# ✅ Global Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"🚨 Validation Error: {exc}")
    return JSONResponse(status_code=422, content={"error": "Invalid input data", "details": exc.errors()})

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"🔥 Unexpected Server Error: {exc}")
    return JSONResponse(status_code=500, content={"error": "Internal Server Error", "details": str(exc)})

# ✅ Lifecycle Events
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Server is starting...")
    logger.info(f"✅ Frontend Allowed: {FRONTEND_URL}")
    logger.info(f"✅ Listening on PORT: {PORT}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Server is shutting down...")

# ✅ Run Uvicorn with Improved Configuration
if __name__ == "__main__":
    logger.info("🌍 Starting Resume AI API...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True, log_level="info")
