from typing import List, Optional
from sqlmodel import select
from sqlalchemy.orm import Session  
from app.database.db import get_session  
from app.models.base import User
from app.schemas.user import UserCreate, UserUpdate, UserOut
from passlib.context import CryptContext
from fastapi import Depends  

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(user_in: UserCreate, session: Session) -> UserOut:  

    existing_email = session.exec(select(User).where(
        (User.email == user_in.email))).first()
    if existing_email :
        raise ValueError("Email already registered")
    
    existing_username = session.exec(select(User).where(
        (User.username == user_in.username))).first()
    if existing_username:
        raise ValueError("Username already registered")
    

    hashed_password = get_password_hash(user_in.password)

    db_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
        gender=user_in.gender,
        birthdate=user_in.birthdate,
        height_cm=user_in.height_cm,
        weight_kg=user_in.weight_kg,
        body_fat_percentage=user_in.body_fat_percentage,
        activity_level=user_in.activity_level,
        goal=user_in.goal
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return UserOut.model_validate(db_user)

def get_user(user_id: int, session: Session) -> Optional[UserOut]:  
    user = session.get(User, user_id)
    if user:
        return UserOut.model_validate(user)
    return None

def get_users(session: Session, offset: int = 0, limit: int = 100) -> List[UserOut]:  
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return [UserOut.model_validate(u) for u in users]

def update_user(user_id: int, user_update: UserUpdate, session: Session) -> Optional[UserOut]:
    user = session.get(User, user_id)  
    if not user:
        return None
    update_data = user_update.dict(exclude_unset=True, exclude={"password"})  
    for field, value in update_data.items():
        setattr(user, field, value) 
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserOut.model_validate(user)

def delete_user(user_id: int, session: Session) -> bool: 
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True