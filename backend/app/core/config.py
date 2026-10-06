from typing import List, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "UNSAID API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    SECRET_KEY: str = "CHANGE-ME-IN-PRODUCTION"  # Override via .env
    
    # LLM Settings
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    
    # Database
    DATABASE_URL: str = "sqlite:///./unsaid.db" # Default to sqlite for local dev
    
    class Config:
        env_file = ".env"

settings = Settings()
