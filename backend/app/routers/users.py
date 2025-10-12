from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database.db import get_session
from app.crud.user import create_user, get_user, get_users, update_user, delete_user
from app.crud.user_exercise_log import get_user_exercise_logs
from app.schemas.user import UserCreate, UserList, UserOut, UserUpdate
from app.schemas.user_exercise_log import UserExerciseLogOut

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_new_user(user_in: UserCreate, session: Session = Depends(get_session)):
    try:
        return create_user(user_in, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/{user_id}", response_model=UserOut)  # GET /users/1
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = get_user(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=UserList)  # GET /users
def read_users(offset: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    users = get_users(session, offset, limit)  
    return {"users": users, "total": len(users)}  

@router.put("/{user_id}", response_model=UserOut)  # PUT /users/1
def update_existing_user(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    updated = update_user(user_id, user_update, session)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)  # DELETE /users/1, no body
def delete_existing_user(user_id: int, session: Session = Depends(get_session)):
    deleted = delete_user(user_id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return None  # 204 = OK, no content

@router.get("/{user_id}/logs", response_model=List[UserExerciseLogOut])
def read_user_logs(user_id: int, offset: int = 0, limit: int = 100, exercise_id: Optional[int] = None, session: Session = Depends(get_session)):
    logs = get_user_exercise_logs(session, user_id, offset, limit, exercise_id)  # <--- Session premier
    return logs