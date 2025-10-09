from fastapi import FastAPI
import sys
import os
from sqlalchemy import text
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.database.config import settings
from app.database.db import engine, get_session

from app.models.base import User
from datetime import datetime
from app.models.base import Gender
from app.models.base import ActivityLevel
from app.models.base import Goal
from app.schemas.user import UserCreate  


app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}

@app.get("/health/db")
def health_db():
    session_gen = get_session()
    session = next(session_gen)
    try:
        result = session.exec(text("SELECT 1")).one()
        return {"db": "ok", "result": result}
    finally:
        session.close()
