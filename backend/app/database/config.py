from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pydantic import field_validator
class Settings(BaseSettings):
    """
    Pydantic lit automatiquement les variables d'environnement
    et celles du fichier .env pour remplir ces champs.
    """
    PROJECT_NAME: str = "GymApp"
    API_PREFIX: str = "/api"

    SQLALCHEMY_DATABASE_URI: str = Field(alias='DATABASE_URL')
    
    SECRET_KEY: str

    ALLOW_ORIGINS: str
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()