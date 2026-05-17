"""
Application configuration using Pydantic Settings
Manages all environment variables and app settings
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Main application settings"""
    
    # Database
    database_url: str = "sqlite:///./simplif_iq.db"
    
    # APIs
    gemini_api_key: str = ""
    openai_api_key: Optional[str] = None
    tavily_api_key: str = ""
    sendgrid_api_key: str = ""
    
    # Email
    from_email: str = "noreply@simplif-iq.com"
    support_email: str = "support@simplif-iq.com"
    
    # Frontend
    frontend_url: str = "http://localhost:5173"
    
    # Google APIs
    google_sheets_api_key: Optional[str] = None
    google_drive_api_key: Optional[str] = None
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings()
