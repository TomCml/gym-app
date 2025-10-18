from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.db import get_session
from app.crud import user_exercise_log as crud_logs
from app.schemas.user_exercise_log import UserExerciseLogCreate, UserExerciseLogOut

router = APIRouter()

@router.post("/", response_model=UserExerciseLogOut, status_code=status.HTTP_201_CREATED)
def create_new_log(log_in: UserExerciseLogCreate, user_id: int, session: Session = Depends(get_session)):
    return crud_logs.create_log(log_in=log_in, user_id=user_id, session=session)