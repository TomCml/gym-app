from pydantic import BaseModel
from typing import Optional, List
from app.models.base import WorkoutExercise, Workout, Exercise  

class WorkoutExerciseCreate(BaseModel):
    exercise_id: int  # FK exercise
    planned_sets: Optional[int] = None
    planned_reps: Optional[int] = None
    planned_weight: Optional[float] = None  
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None

class WorkoutExerciseUpdate(BaseModel):
    planned_sets: Optional[int] = None
    planned_reps: Optional[int] = None
    planned_weight: Optional[float] = None
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None

class WorkoutExerciseOut(BaseModel):
    id: int
    workout_id: int
    exercise_id: int
    planned_sets: Optional[int]
    planned_reps: Optional[int]
    planned_weight: Optional[float]
    rest_seconds: Optional[int]
    notes: Optional[str]
    workout: Workout  
    exercise: Exercise  

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True 

class AddExercisesToWorkout(BaseModel):  
    exercises: List[WorkoutExerciseCreate]  