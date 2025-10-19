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

    DATABASE_URL: str
    
    SECRET_KEY: str

    ALLOW_ORIGINS: List[str] 
    @field_validator('ALLOW_ORIGINS', mode='before')
    @classmethod
    def _split_str(cls, v):
        if isinstance(v, str):
            return [item.strip() for item in v.split(',') if item.strip()]
        return v

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()