from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional
from jose import JWTError, jwt
from datetime import timedelta, datetime, timezone # Import timezone
from sqlalchemy.orm import Session
from sqlalchemy import select, func # Import func for COUNT
from app.database.db import get_session
from app.models.base import User
from app.crud.user import create_user, get_user, get_users, update_user, delete_user, pwd_context
from app.crud.user_exercise_log import get_user_exercise_logs
from app.schemas.user import UserCreate, UserList, UserOut, UserUpdate, TokenData
from app.schemas.user_exercise_log import UserExerciseLogOut
import os

router = APIRouter()

# --- Configuration de l'Authentification ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login") # URL complète pour la clarté
SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key_that_should_be_long_and_random")
ALGORITHM = "HS256"
# 💡 Conseil : 84 jours, c'est très long. Pense à un temps plus court (ex: 1 jour)
# et à implémenter un système de "refresh token" pour une meilleure sécurité.
ACCESS_TOKEN_EXPIRE_MINUTES = 120960 # 84 jours

# --- Fonctions Utilitaires pour le Token ---
def create_access_token(data: dict):
    to_encode = data.copy()
    # Utilise timezone.utc pour éviter les problèmes de fuseaux horaires
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- Dépendance pour obtenir l'utilisateur courant ---
def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    user = session.get(User, token_data.user_id)
    if user is None:
        raise credentials_exception
    return user

# --- Routes Publiques (Création et Connexion) ---

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_new_user(user_in: UserCreate, session: Session = Depends(get_session)):
    existing_email = session.exec(
        select(User).where(User.email == user_in.email)
    ).first()
    if existing_email:
        raise HTTPException(status_code=409, detail="Email already registered")

    existing_username = session.exec(
        select(User).where(User.username == user_in.username)
    ).first()
    if existing_username:
        raise HTTPException(status_code=409, detail="Username already registered")
    
    user = create_user(user_in, session)
    return user

@router.post("/login", summary="User login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """
    Connecte l'utilisateur et retourne un token JWT.
    """
    user = session.exec(select(User).where(User.email == form_data.username)).scalar()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": str(user.id)}) 
    
    return {"access_token": access_token, "token_type": "bearer", "user": UserOut.model_validate(user)}

# --- Routes Protégées (Nécessitent une authentification) ---

@router.get("/me", response_model=UserOut, summary="Get current user's data")
def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Récupère les informations de l'utilisateur actuellement connecté.
    """
    return current_user

@router.get("/", response_model=UserList, summary="Get a list of users")
def read_users(
    session: Session = Depends(get_session), 
    offset: int = 0, 
    limit: int = 100,
    # 🔒 Seuls les utilisateurs authentifiés peuvent voir la liste
    current_user: User = Depends(get_current_user) 
):
    """
    Récupère une liste paginée d'utilisateurs.
    """
    users = get_users(session, offset, limit)
    # ✨ CORRECTION : Compte le nombre total d'utilisateurs dans la base de données
    total_users = session.exec(select(func.count(User.id))).one()
    return {"users": users, "total": total_users}

@router.get("/{user_id}", response_model=UserOut, summary="Get user by ID")
def read_user(user_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """
    Récupère les informations d'un utilisateur par son ID.
    """
    user = get_user(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/me", response_model=UserOut, summary="Update current user's data")
def update_current_user(
    user_update: UserUpdate, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    """
    Met à jour les informations de l'utilisateur actuellement connecté.
    """
    updated_user = update_user(current_user.id, user_update, session)
    if not updated_user:
        
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT, summary="Delete current user")
def delete_current_user(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """
    Supprime le compte de l'utilisateur actuellement connecté.
    """
    delete_user(current_user.id, session)
    return None

@router.get("/{user_id}/logs", response_model=List[UserExerciseLogOut], summary="Get exercise logs for a user")
def read_user_logs(
    user_id: int,
    offset: int = 0,
    limit: int = 100,
    exercise_id: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les logs d'exercices pour un utilisateur spécifique.
    🔒 Seul un utilisateur peut voir ses propres logs (ou un admin).
    """
    if current_user.id != user_id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access these logs")
    
    logs = get_user_exercise_logs(session, user_id, offset, limit, exercise_id)
    return logs