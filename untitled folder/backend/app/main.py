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


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
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
