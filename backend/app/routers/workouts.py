from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database.db import get_session
from app.crud.workouts import create_workout, get_workout, get_workouts, update_workout, delete_workout
from app.crud.user_exercise_log import get_user_exercise_logs, add_logs_to_workout
from app.schemas.workouts import WorkoutCreate, WorkoutUpdate, WorkoutOut, WorkoutList,  Workout
from app.schemas.workout_exercises import WorkoutExerciseOut, AddExercisesToWorkout 
from app.schemas.user_exercise_log import UserExerciseLogOut, AddLogsToWorkout


router = APIRouter()

@router.post("/", response_model=WorkoutOut, status_code=status.HTTP_201_CREATED)
def create_new_workout(workout_in: WorkoutCreate, session: Session = Depends(get_session)):
    try:
        return create_workout(workout_in, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{workout_id}", response_model=WorkoutOut)
def read_workout(workout_id: int, session: Session = Depends(get_session)):
    workout = get_workout(workout_id, session)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

@router.get("/", response_model=WorkoutList)
def read_workouts(offset: int = 0, limit: int = 100, user_id: Optional[int] = None, session: Session = Depends(get_session)):
    workouts = get_workouts(session, offset, limit, user_id)  
    return {"workouts": workouts, "total": len(workouts)}

@router.put("/{workout_id}", response_model=WorkoutOut)
def update_existing_workout(workout_id: int, workout_update: WorkoutUpdate, session: Session = Depends(get_session)):
    updated = update_workout(workout_id, workout_update, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Workout not found")
    return updated

@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_workout(workout_id: int, session: Session = Depends(get_session)):
    deleted = delete_workout(workout_id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Workout not found")
    return None

@router.post("/{workout_id}/exercises", response_model=List[WorkoutExerciseOut])
def add_exercises_to_workout(workout_id: int, data: AddExercisesToWorkout, session: Session = Depends(get_session)):
    try:
        return add_exercises_to_workout(workout_id, data, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{workout_id}/exercises", response_model=List[WorkoutExerciseOut])
def get_workout_exercises(workout_id: int, session: Session = Depends(get_session)):
    exercises = get_workout_exercises(workout_id, session)
    if not exercises:
        raise HTTPException(status_code=404, detail="No exercises for this workout")
    return exercises

@router.post("/{workout_id}/logs", response_model=List[UserExerciseLogOut])
def add_logs_to_workout_endpoint(workout_id: int, user_id: int, data: AddLogsToWorkout, session: Session = Depends(get_session)):
    try:
        return add_logs_to_workout(user_id, workout_id, data, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{workout_id}/logs", response_model=List[UserExerciseLogOut])
def read_workout_logs(workout_id: int, session: Session = Depends(get_session)):
    workout = session.get(Workout, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    logs = get_user_exercise_logs(
        session=session,  
        user_id=workout.user_id,  
        workout_id=workout_id  
    )
    return logs