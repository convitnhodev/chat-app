from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_TITLE: str = "FastAPI Project"  # This will be overridden by env var
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "FastAPI Project with proper configuration"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DATABASE_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "my_database"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    class Config:
        env_file = ".env" 
        case_sensitive = True

settings = Settings() 