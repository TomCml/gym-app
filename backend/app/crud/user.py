from typing import List, Optional
from sqlmodel import select
from sqlalchemy.orm import Session  
from app.database.db import get_session  
from app.models.base import User
from app.schemas.user import UserCreate, UserUpdate, UserOut
from passlib.context import CryptContext  

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_user