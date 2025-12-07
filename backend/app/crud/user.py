from typing import List, Optional
from sqlmodel import select
from sqlalchemy.orm import Session
from app.models.base import User
from app.schemas.user import UserCreate, UserUpdate, UserOut
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(user_in: UserCreate, session: Session) -> User:
    hashed_password = get_password_hash(user_in.password)

    user_data = user_in.model_dump(exclude={"password"})
    # normalize field name coming from schema -> model
    if "body_fat_percentage" in user_data:
        user_data["body_fat"] = user_data.pop("body_fat_percentage")
    db_user = User(**user_data, hashed_password=hashed_password)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user(user_id: int, session: Session) -> Optional[User]:
    return session.get(User, user_id)

def get_users(session: Session, offset: int = 0, limit: int = 100) -> List[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

def update_user(user_id: int, user_update: UserUpdate, session: Session) -> Optional[User]:
    user = session.get(User, user_id)
    if not user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    # normalize field name if frontend sends body_fat_percentage
    if "body_fat_percentage" in update_data:
        update_data["body_fat"] = update_data.pop("body_fat_percentage")

    
    # --- VÉRIFICATION UNIQUE (EMAIL) ---
    if "email" in update_data and update_data["email"] != user.email:
        existing_user = session.exec(
            select(User).where(User.email == update_data["email"])
        ).first()
        if existing_user:
            raise ValueError(f"L'email {update_data['email']} est déjà pris.")
    
    if "username" in update_data and update_data["username"] != user.username:
        existing_user = session.exec(
            select(User).where(User.username == update_data["username"])
        ).first()
        if existing_user:
            raise ValueError(f"Le nom d'utilisateur {update_data['username']} est déjà pris.")

    if "birthdate" in update_data and isinstance(update_data["birthdate"], str):
        try:
            update_data["birthdate"] = datetime.fromisoformat(
                update_data["birthdate"].replace('Z', '+00:00')
            )
        except ValueError:
            raise ValueError("Format de date invalide. Attendu format ISO.")

    for field, value in update_data.items():
        if field != "password":  
            setattr(user, field, value)
            
    user.updated_at = datetime.utcnow() 

    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except Exception as e:
        session.rollback()
        raise e 
        
    return user

def update_user_password(user: User, new_password: str, session: Session) -> User:
    """Met à jour le mot de passe d'un utilisateur."""
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def delete_user(user_id: int, session: Session) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True