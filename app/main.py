import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from app.routes import router  # ✅ Ensure correct import

# ✅ Set up Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Initialize FastAPI App with Metadata
app = FastAPI(
    title="Timothy Riffe Resume AI",
    description="AI-driven resume generation and PDF conversion API.",
    version="1.0.0"
)

# ✅ Include Routes
app.include_router(router)

# ✅ Global Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles request validation errors and returns structured JSON responses.
    """
    logger.error(f"Validation Error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid input data", "details": exc.errors()}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Handles unexpected server errors and logs them for debugging.
    """
    logger.error(f"🔥 Unexpected Server Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "details": str(exc)}
    )

# ✅ Lifecycle Events (Ensure Safe Startup & Shutdown)
@app.on_event("startup")
async def startup_event():
    """
    Called when the application starts. Can be used to initialize resources.
    """
    logger.info("🚀 Server is starting...")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Called when the application is shutting down. Can be used for cleanup.
    """
    logger.info("🛑 Server is shutting down...")

# ✅ Run Uvicorn with Improved Configuration
if __name__ == "__main__":
    logger.info("🌍 Starting Resume AI API...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # ✅ Auto-reload for development
        log_level="info"
    )
