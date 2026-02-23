from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application configuration"""

    # Application
    APP_NAME: str = "OSINT Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str
    REDIS_URL: str

    # OSINT APIs
    SHODAN_API_KEY: Optional[str] = None
    VIRUSTOTAL_API_KEY: Optional[str] = None
    GITHUB_TOKEN: Optional[str] = None
    HUNTER_IO_KEY: Optional[str] = None
    HIBP_API_KEY: Optional[str] = None
    CENSYS_API_ID: Optional[str] = None
    CENSYS_API_SECRET: Optional[str] = None

    # AI Configuration
    AI_MODEL_PATH: str = "./models"
    USE_GPU: bool = False
    HF_TOKEN: Optional[str] = None

    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # Security
    SECRET_KEY: str
    JWT_SECRET_KEY: str = "change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
