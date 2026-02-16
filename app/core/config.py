from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    """Application Configuration"""
    
    # App Info
    APP_NAME: str = "Smart Recruit AI"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # File Upload
    UPLOAD_FOLDER: str = "./uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    MAX_FILES_PER_UPLOAD: int = 1000
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".doc"]
    
    # AI Models
    NAME_EXTRACTION_MODEL: str = "timpal0l/mdeberta-v3-base-squad2"
    SCORING_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"
    ACCEPTANCE_THRESHOLD: float = 0.45
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    @property
    def cors_origins(self) -> List[str]:
        """Convert comma-separated origins to list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance"""
    return Settings()
