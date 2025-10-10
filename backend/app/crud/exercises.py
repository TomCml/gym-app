from typing import List, Optional
from sqlmodel import select
from sqlalchemy import func  
from sqlalchemy.orm import Session
from app.database.db import get_session
from app.models.base import Exercise
from app.schemas.exercises import ExerciseCreate, ExerciseUpdate, ExerciseOut

def create_exercise(exercise_in: ExerciseCreate, session: Session) -> ExerciseOut:

    existing = session.exec(select(Exercise).where(Exercise.name == exercise_in.name)).first()
    if existing:
        raise ValueError("Exercise already exists")

    db_exercise = Exercise(
        name=exercise_in.name,
        description=exercise_in.description,
        muscle_group=exercise_in.muscle_group,
        equipement=exercise_in.equipement,
        difficulty=exercise_in.difficulty,
        is_cardio=exercise_in.is_cardio
    )
    session.add(db_exercise)
    session.commit()
    session.refresh(db_exercise)
    return ExerciseOut.model_validate(db_exercise)

def get_exercise(exercise_id: int, session: Session) -> Optional[ExerciseOut]:
    exercise = session.get(Exercise, exercise_id)
    if exercise:
        return ExerciseOut.model_validate(exercise)
    return None

def get_exercises(session: Session, offset: int = 0, limit: int = 100 ) -> List[ExerciseOut]:
    exercises = session.exec(select(Exercise).offset(offset).limit(limit)).all()
    return [ExerciseOut.model_validate(e) for e in exercises]

def update_exercise(exercise_id: int, exercise_update: ExerciseUpdate, session: Session) -> Optional[ExerciseOut]:
    exercise = session.get(Exercise, exercise_id)
    if not exercise:
        return None
    update_data = exercise_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(exercise, field, value)
    session.add(exercise)
    session.commit()
    session.refresh(exercise)
    return ExerciseOut.model_validate(exercise)

def delete_exercise(exercise_id: int, session: Session) -> bool:
    exercise = session.get(Exercise, exercise_id)
    if not exercise:
        return False
    session.delete(exercise)
    session.commit()
    return True


def get_exercise_by_name(name: str, session: Session) -> List[ExerciseOut]:
    exercises = session.exec(
        select(Exercise).where(func.unaccent(Exercise.name).ilike(f"%{name}%"))  
    ).all()
    return [ExerciseOut.from_orm(e) for e in exercises]

def get_exercises_by_muscle_group(muscle_group: str, session: Session) -> List[ExerciseOut]:
    exercises = session.exec(
        select(Exercise).where(Exercise.muscle_group == muscle_group)  
    ).all()
    return [ExerciseOut.model_validate(e) for e in exercises]

def get_cardio_exercises(session: Session) -> List[ExerciseOut]:
    exercises = session.exec(
        select(Exercise).where(Exercise.is_cardio == True)  
    ).all()
    return [ExerciseOut.model_validate(e) for e in exercises]