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
    
    # APIs — at least one LLM key (Gemini or OpenAI) is needed for AI insights.
    # If both are set, Gemini wins (free-tier friendly).
    gemini_api_key: Optional[str] = None
    gemini_model: str = "gemini-2.5-flash"
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    tavily_api_key: str = ""
    sendgrid_api_key: str = ""
    
    # Email
    from_email: str = "noreply@simplif-iq.com"
    support_email: str = "support@simplif-iq.com"
    
    # Frontend
    frontend_url: str = "http://localhost:5173"
    
    # Google APIs — service account auth (preferred for server-to-server)
    google_service_account_file: Optional[str] = None
    google_sheets_spreadsheet_id: Optional[str] = None
    google_sheets_sheet_name: str = "Leads"
    google_drive_folder_id: Optional[str] = None
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # tolerate stale keys (e.g. GEMINI_API_KEY) in old .env files


# Create settings instance
settings = Settings()
