from typing import List, Optional
from sqlmodel import select
from sqlalchemy.orm import Session
from app.models.base import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(user_in: UserCreate, session: Session) -> User:
    hashed_password = get_password_hash(user_in.password)

    user_data = user_in.model_dump(exclude={"password"})
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
    
    for field, value in update_data.items():
        if field != "password":
            setattr(user, field, value)
            
    session.add(user)
    session.commit()
    session.refresh(user)
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