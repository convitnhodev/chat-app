from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_TITLE: str = "FastAPI Project"  # This will be overridden by env var
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "FastAPI Project with proper configuration"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    class Config:
        env_file = ".env" 
        case_sensitive = True

settings = Settings() 