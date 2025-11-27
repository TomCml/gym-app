from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional
from jose import JWTError, jwt
from datetime import timedelta, datetime, timezone  # Import timezone
from sqlalchemy.orm import Session
from sqlalchemy import select, func  # Import func for COUNT
from ..database.db import get_session
from ..models.base import User
from ..crud.workouts import create_default_workouts
from ..crud.user import (
    create_user,
    get_user,
    get_users,
    update_user,
    delete_user,
    pwd_context,
    update_user_password,
)
from ..crud.user_exercise_log import get_user_exercise_logs
from ..schemas.user import (
    UserCreate,
    UserList,
    UserOut,
    UserUpdate,
    TokenData,
    PasswordChange,
)
from ..schemas.user_exercise_log import UserExerciseLogOut
import os

router = APIRouter()

# --- Configuration de l'Authentification ---
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/users/login"
)  # URL complète pour la clarté
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120960  # 84 jours


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: Optional[str] = payload.get("sub")
        if sub is None:
            raise credentials_exception
        try:
            user_id = int(sub)
        except (ValueError, TypeError):
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
    try:
        
        create_default_workouts(db=session, user_id=user.id)

    except Exception as e:
        print(f"ATTENTION: L'utilisateur {user.email} a été créé, mais la création des workouts de base a échoué: {e}")
    
    return user


@router.post("/login", summary="User login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    """
    Connecte l'utilisateur et retourne un token JWT.
    """
    user = session.exec(select(User).where(User.email == form_data.username)).scalar()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserOut.model_validate(user),
    }


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
    current_user: User = Depends(get_current_user),
):
    """
    Récupère une liste paginée d'utilisateurs.
    """
    users = get_users(session, offset, limit)
    total_users = session.exec(select(func.count(User.id))).one()
    return {"users": users, "total": total_users}


@router.get("/{user_id}", response_model=UserOut, summary="Get user by ID")
def read_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
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
    current_user: User = Depends(get_current_user),
):
    """
    Met à jour les informations de l'utilisateur actuellement connecté.
    """
    assert current_user.id is not None
    updated_user = update_user(current_user.id, user_update, session)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.put(
    "/me/password",
    status_code=status.HTTP_200_OK,
    summary="Change current user's password",
)
def change_password(
    password_data: PasswordChange,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Change le mot de passe de l'utilisateur actuellement connecté.
    Nécessite le mot de passe actuel et le nouveau mot de passe.
    """
    # Vérifier que le mot de passe actuel est correct
    if not pwd_context.verify(
        password_data.current_password, current_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    # Vérifier que le nouveau mot de passe est différent de l'ancien
    if password_data.current_password == password_data.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password",
        )

    # Mettre à jour le mot de passe
    update_user_password(current_user, password_data.new_password, session)

    return {"message": "Password updated successfully"}


@router.delete(
    "/me", status_code=status.HTTP_204_NO_CONTENT, summary="Delete current user"
)
def delete_current_user(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Supprime le compte de l'utilisateur actuellement connecté.
    """
    assert current_user.id is not None
    delete_user(current_user.id, session)
    return None


@router.get(
    "/{user_id}/logs",
    response_model=List[UserExerciseLogOut],
    summary="Get exercise logs for a user",
)
def read_user_logs(
    user_id: int,
    offset: int = 0,
    limit: int = 100,
    exercise_id: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these logs",
        )

    logs = get_user_exercise_logs(session, user_id, offset, limit, exercise_id)
    return logs
