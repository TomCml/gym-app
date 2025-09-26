import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(project_root / ".env")

print(f"DB_USER: {os.environ.get('POSTGRES_USER')}")
print(f"DB_HOST: {os.environ.get('POSTGRES_HOST')}")
print(f"DB_NAME: {os.environ.get('POSTGRES_DB')}")

class Settings(BaseModel):
    PROJECT_NAME: str = "GymApp"
    API_PREFIX: str = "/api"

    DB_USER: str = os.environ["POSTGRES_USER"]
    DB_PASSWORD: str = os.environ["POSTGRES_PASSWORD"]
    DB_HOST: str = os.environ["POSTGRES_HOST"]
    DB_PORT: str = os.environ["POSTGRES_PORT"]
    DB_NAME: str = os.environ["POSTGRES_DB"]

    SQLALCHEMY_DATABASE_URI: str = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD.replace('@', '%40')}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    ALLOW_ORIGINS: list[str] = os.getenv("ALLOW_ORIGINS", "*").split(",")

settings = Settings()
