import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "SupportPilot AI"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
    
    # Email Settings
    EMAIL_HOST: str = os.getenv("EMAIL_HOST", "imap.gmail.com")
    EMAIL_PORT: int = int(os.getenv("EMAIL_PORT", 993))
    EMAIL_USER: str = os.getenv("EMAIL_USER", "")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "")
    
    # AI Settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    class Config:
        env_file = "../.env"

settings = Settings()
