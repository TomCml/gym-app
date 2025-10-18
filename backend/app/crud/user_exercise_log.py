from typing import List, Optional
from sqlmodel import select
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.db import get_session
from app.models.base import UserExerciseLog, User, Exercise, Workout
from app.schemas.user_exercise_log import UserExerciseLogCreate, UserExerciseLogUpdate, UserExerciseLogOut, AddLogsToWorkout

def create_user_exercise_log(log_in: UserExerciseLogCreate, session: Session) -> UserExerciseLogOut:
    user = session.get(User, log_in.user_id)  # Assumé user_id toujours fourni
    if not user:
        raise ValueError("User not found")
    exercise = session.get(Exercise, log_in.exercise_id)
    if not exercise:
        raise ValueError("Exercise not found")
    if log_in.workout_id:
        workout = session.get(Workout, log_in.workout_id)
        if not workout:
            raise ValueError("Workout not found")

    volume = log_in.volume or (log_in.reps * log_in.weight or 0)  

    db_log = UserExerciseLog(
        user_id=log_in.user_id,
        exercise_id=log_in.exercise_id,
        workout_id=log_in.workout_id,
        date=datetime.now(),  # Ou log_in.date si fourni
        set_number=log_in.set_number,
        reps=log_in.reps,
        weight=log_in.weight,
        rest_seconds=log_in.rest_seconds,
        duration_seconds=log_in.duration_seconds,
        distance_m=log_in.distance_m,
        volume=volume,
        notes=log_in.notes
    )
    session.add(db_log)
    session.commit()
    session.refresh(db_log)
    return UserExerciseLogOut.model_validate(db_log)

def add_logs_to_workout(session: Session, user_id: int, workout_id: Optional[int], logs_data: AddLogsToWorkout ) -> List[UserExerciseLogOut]:
    added = []
    for log_in in logs_data.logs:
        log_in.user_id = user_id  
        log_in.workout_id = workout_id
        added.append(create_user_exercise_log(log_in, session))
    return added

def get_user_exercise_logs(session: Session, user_id: int, offset: int = 0, limit: int = 100, exercise_id: Optional[int] = None, workout_id: Optional[int] = None) -> List[UserExerciseLogOut]:
    query = select(UserExerciseLog).where(UserExerciseLog.user_id == user_id).offset(offset).limit(limit)
    if exercise_id:
        query = query.where(UserExerciseLog.exercise_id == exercise_id)
    logs = session.exec(query).all()
    return [UserExerciseLogOut.model_validate(l) for l in logs]

def update_user_exercise_log(session: Session, log_id: int, log_update: UserExerciseLogUpdate) -> Optional[UserExerciseLogOut]:
    log = session.get(UserExerciseLog, log_id)
    if not log:
        return None
    update_data = log_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(log, field, value)
    session.add(log)
    session.commit()
    session.refresh(log)
    return UserExerciseLogOut.model_validate(log)

def delete_user_exercise_log(session: Session, log_id: int) -> bool:
    log = session.get(UserExerciseLog, log_id)
    if not log:
        return False
    session.delete(log)
    session.commit()
    return True

def create_log(log_in: UserExerciseLogCreate, user_id: int, session: Session) -> UserExerciseLogOut:
    log_data = log_in.model_dump()
    db_log = UserExerciseLog(**log_data, user_id=user_id)
    session.add(db_log)
    session.commit()
    session.refresh(db_log)
    return UserExerciseLogOut.model_validate(db_log)