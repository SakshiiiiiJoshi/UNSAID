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
    GEMINI_MODEL: str = "gemini-3.8-flash"  # Override in .env if needed

    # Database — must use asyncpg driver for async FastAPI
    # Format: postgresql+asyncpg://user:password@host:port/dbname
    DATABASE_URL: str = "postgresql+asyncpg://unsaid:unsaid@localhost:5432/unsaid"

    class Config:
        env_file = ".env"


settings = Settings()
