from fastapi import FastAPI
from sqlalchemy import text
from src.app.database.config import settings
from src.app.database.db import engine

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/healthz")
def healthz():
	return {"ok": True}

@app.get("/")
def root():
	return {"message": "Hello from FastAPI"}

@app.get("/health/db")
def health_db():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"db": "ok"}