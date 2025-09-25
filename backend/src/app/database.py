import os
from pydrantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "GymApp"
    API_PREFIX: str = "/api"
    DB_USER: str = os.getenv("POSTGRES_USER", "app")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "app")
    DB_HOST: str = os.getenv("POSTGRES_HOST", "db")
    DB_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    DB_NAME: str = os.getenv("POSTGRES_DB", "app")
