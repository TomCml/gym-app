# Fichier: app/database/config.py (ou où que soit ton config.py)

# 1. On importe depuis pydantic_settings
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    """
    Pydantic lit automatiquement les variables d'environnement
    et celles du fichier .env pour remplir ces champs.
    """
    PROJECT_NAME: str = "GymApp"
    API_PREFIX: str = "/api"

    DATABASE_URL: str
    
    SECRET_KEY: str

    ALLOW_ORIGINS: List[str] 

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()