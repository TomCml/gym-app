from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database.db import get_session
from app.crud.exercises import create_exercise, get_exercise, get_exercises, update_exercise, delete_exercise, get_exercise_by_name, get_exercises_by_muscle_group, get_cardio_exercises
from app.schemas.exercises import ExerciseCreate, ExerciseUpdate, ExerciseOut, ExerciseList

router = APIRouter()

@router.post("/", response_model=ExerciseOut, status_code=status.HTTP_201_CREATED)
def create_new_exercise(exercise_in: ExerciseCreate, session: Session = Depends(get_session)):
    try:
        return create_exercise(exercise_in, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{exercise_id}", response_model=ExerciseOut)
def read_exercise(exercise_id: int, session: Session = Depends(get_session)):
    exercise = get_exercise(exercise_id, session)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

@router.get("/", response_model=ExerciseList)
def read_exercises(offset: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    exercises = get_exercises(session, offset, limit)
    return {"exercises": exercises, "total": len(exercises)}

@router.put("/{exercise_id}", response_model=ExerciseOut)
def update_existing_exercise(exercise_id: int, exercise_update: ExerciseUpdate, session: Session = Depends(get_session)):
    updated = update_exercise(exercise_id, exercise_update, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return updated

@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_exercise(exercise_id: int, session: Session = Depends(get_session)):
    deleted = delete_exercise(exercise_id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return None

@router.get("/search/{name}", response_model=List[ExerciseOut])
def search_exercise_by_name(name: str, session: Session = Depends(get_session)):
    return get_exercise_by_name(name, session)

@router.get("/muscle/{muscle_group}", response_model=List[ExerciseOut])
def get_by_muscle_group(muscle_group: str, session: Session = Depends(get_session)):
    return get_exercises_by_muscle_group(muscle_group, session)

@router.get("/cardio", response_model=List[ExerciseOut])
def get_cardio(session: Session = Depends(get_session)):
    return get_cardio_exercises(session)