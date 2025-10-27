from pydantic_settings import BaseSettings, SettingsConfigDict
import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

class Settings(BaseSettings):
    PROJECT_NAME: str = "GymApp"
    API_PREFIX: str = "/api"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SECRET_KEY: str
    ALLOW_ORIGINS: str

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        driver = "psycopg2" 
        return f"postgresql+{driver}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@db:5432/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=".env.dev" if ENVIRONMENT == "development" else ".env.prod",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()