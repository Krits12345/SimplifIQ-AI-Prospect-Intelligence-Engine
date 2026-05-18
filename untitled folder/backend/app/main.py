"""
Main FastAPI application
Entry point for the backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import init_db
from app.routes import leads, admin, reports
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown logic"""
    # Startup
    logger.info("Starting SimplifIQ AI Prospect Intelligence Engine")
    init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down SimplifIQ AI Prospect Intelligence Engine")


# Create FastAPI app
app = FastAPI(
    title="SimplifIQ AI Prospect Intelligence Engine",
    description="AI-powered lead automation and company intelligence platform",
    version="1.0.0",
    lifespan=lifespan
)


# Configure CORS.
# - Local dev: any localhost / 127.0.0.1 port (vite hops 5173 → 5174 → 5175…).
# - Production: any Vercel deploy of this project, including preview URLs
#   (e.g. https://<project>-<hash>-<team>.vercel.app).
# If you move to a custom domain, add it here or set ALLOWED_ORIGIN_REGEX
# explicitly in the Render environment.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"(http://(localhost|127\.0\.0\.1)(:\d+)?|https://([a-z0-9-]+\.)*vercel\.app)",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(leads.router)
app.include_router(admin.router)
app.include_router(reports.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SimplifIQ AI Prospect Intelligence Engine",
        "version": "1.0.0",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SimplifIQ Backend"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
