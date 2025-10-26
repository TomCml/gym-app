from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from typing import List
from pydantic import Field

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # default: dev

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
        driver = "psycopg"  # ou "psycopg2" selon ton driver
        return f"postgresql+{driver}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@db:5432/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=".env.dev" if ENVIRONMENT == "development" else ".env.prod",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instance globale
settings = Settings()