from fastapi import FastAPI
from src.infrastructure.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Unified Registry for LLMs",
)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "database": settings.DATABASE_URL
    }

@app.get("/")
async def root():
    """Root endpoint with documentation link."""
    return {
        "message": "Welcome to LLMIndex API",
        "docs": "/docs"
    }
