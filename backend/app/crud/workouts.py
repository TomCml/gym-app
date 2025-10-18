from typing import List, Optional, Tuple
from sqlmodel import select, func
from sqlalchemy.orm import Session
from datetime import datetime 
from app.database.db import get_session
from app.models.base import Workout, User  # User pour check FK
from app.schemas.workouts import WorkoutCreate, WorkoutUpdate, WorkoutOut
from .workout_exercises import WorkoutExerciseCreate
from app.models.base import Workout, WorkoutExercise 
from sqlmodel import select, delete  

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
    db_workout = session.get(Workout, workout_id)
    if not db_workout:
        return None

    # On extrait les données du payload. exclude_unset=True est important.
    update_data = workout_update.model_dump(exclude_unset=True)

    # 1. Gérer la mise à jour des exercices, s'ils sont fournis
    if "exercises" in update_data:
        new_exercises_data = update_data.pop("exercises") # On les retire pour le traitement

        # a. Supprimer tous les anciens exercices liés à ce workout
        delete_statement = delete(WorkoutExercise).where(WorkoutExercise.workout_id == workout_id)
        session.exec(delete_statement)

        # b. Ajouter les nouveaux exercices
        for exercise_in in new_exercises_data:
            # On peut utiliser model_validate pour convertir le dict en Pydantic model si besoin
            ex_model = WorkoutExerciseCreate.model_validate(exercise_in)
            db_exercise = WorkoutExercise(
                workout_id=workout_id,
                **ex_model.model_dump()
            )
            session.add(db_exercise)

    # 2. Mettre à jour les champs simples du workout (name, notes, etc.)
    for key, value in update_data.items():
        setattr(db_workout, key, value)
    
    session.add(db_workout)
    session.commit()
    session.refresh(db_workout)
    
    return WorkoutOut.model_validate(db_workout)


def get_workout_for_day(user_id: int, day_of_week: int, session: Session) -> Optional[WorkoutOut]:
    """Récupère le premier workout planifié pour un jour donné."""
    workout_db = session.exec(
        select(Workout).where(Workout.user_id == user_id, Workout.day_of_week == day_of_week)
    ).first()
    
    if workout_db:
        return WorkoutOut.model_validate(workout_db)
    return None

def delete_workout(workout_id: int, session: Session) -> bool:
    workout = session.get(Workout, workout_id)
    if not workout:
        return False
    session.delete(workout)
    session.commit()
    return True