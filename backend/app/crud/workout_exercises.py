from typing import List, Optional
from sqlmodel import select
from sqlalchemy.orm import Session
from app.database.db import get_session
from app.models.base import WorkoutExercise, Workout, Exercise
from app.schemas.workout_exercises import WorkoutExerciseCreate, WorkoutExerciseUpdate, WorkoutExerciseOut, AddExercisesToWorkout  # <--- AJOUT COMPLET

def create_workout_exercise(exercise_in: WorkoutExerciseCreate, workout_id: int, session: Session) -> WorkoutExerciseOut:

    workout = session.get(Workout, workout_id)
    if not workout:
        raise ValueError("Workout not found")
    exercise = session.get(Exercise, exercise_in.exercise_id)
    if not exercise:
        raise ValueError("Exercise not found")

    db_exercise = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_in.exercise_id,
        planned_sets=exercise_in.planned_sets,
        planned_reps=exercise_in.planned_reps,
        planned_weight=exercise_in.planned_weight,
        rest_seconds=exercise_in.rest_seconds,
        notes=exercise_in.notes
    )
    session.add(db_exercise)
    session.commit()
    session.refresh(db_exercise)  # Charge relations
    return WorkoutExerciseOut.model_validate(db_exercise)

def add_exercises_to_workout(workout_id: int, exercises_data: AddExercisesToWorkout, session: Session) -> List[WorkoutExerciseOut]:
    added = []
    for exercise_in in exercises_data.exercises:
        added.append(create_workout_exercise(exercise_in, workout_id, session))
    return added

def get_workout_exercises(workout_id: int, session: Session) -> List[WorkoutExerciseOut]:
    exercises = session.exec(
        select(WorkoutExercise).where(WorkoutExercise.workout_id == workout_id)
    ).all()
    return [WorkoutExerciseOut.model_validate(e) for e in exercises]

def update_workout_exercise(exercise_id: int, exercise_update: WorkoutExerciseUpdate, session: Session) -> Optional[WorkoutExerciseOut]:
    exercise = session.get(WorkoutExercise, exercise_id)
    if not exercise:
        return None
    update_data = exercise_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(exercise, field, value)
    session.add(exercise)
    session.commit()
    session.refresh(exercise)
    return WorkoutExerciseOut.model_validate(exercise)

def delete_workout_exercise(exercise_id: int, session: Session) -> bool:
    exercise = session.get(WorkoutExercise, exercise_id)
    if not exercise:
        return False
    session.delete(exercise)
    session.commit()
    return True