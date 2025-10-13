from typing import List, Optional, Tuple
from sqlmodel import select, func
from sqlalchemy.orm import Session
from app.database.db import get_session
from app.models.base import Workout, User  # User pour check FK
from app.schemas.workouts import WorkoutCreate, WorkoutUpdate, WorkoutOut

def create_workout(workout_in: WorkoutCreate, session: Session) -> WorkoutOut:
    owner = session.get(User, workout_in.user_id)
    if not owner:
        raise ValueError("User not found")

    db_workout = Workout(
        name=workout_in.name,
        date=workout_in.date,
        notes=workout_in.notes,
        user_id=workout_in.user_id
    )
    session.add(db_workout)
    session.commit()
    session.refresh(db_workout)  
    return WorkoutOut.model_validate(db_workout)

def get_workout(workout_id: int, session: Session) -> Optional[WorkoutOut]:
    workout = session.get(Workout, workout_id)
    if workout:
        return WorkoutOut.model_validate(workout)
    return None

def get_workouts(
    session: Session, offset: int, limit: int, user_id: Optional[int] = None
) -> Tuple[List[WorkoutOut], int]:
    
    count_statement = select(func.count(Workout.id))
    if user_id:
        count_statement = count_statement.where(Workout.user_id == user_id)
    
    total = session.exec(count_statement).one()

    data_statement = select(Workout).offset(offset).limit(limit)
    if user_id:
        data_statement = data_statement.where(Workout.user_id == user_id)

    workouts_db = session.exec(data_statement).all()
    
    workouts_out = [WorkoutOut.model_validate(w) for w in workouts_db]

    return workouts_out, total

def update_workout(workout_id: int, workout_update: WorkoutUpdate, session: Session) -> Optional[WorkoutOut]:
    workout = session.get(Workout, workout_id)
    if not workout:
        return None
    update_data = workout_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(workout, field, value)
    session.add(workout)
    session.commit()
    session.refresh(workout)
    return WorkoutOut.model_validate(workout)

def delete_workout(workout_id: int, session: Session) -> bool:
    workout = session.get(Workout, workout_id)
    if not workout:
        return False
    session.delete(workout)
    session.commit()
    return True