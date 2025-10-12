from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.base import UserExerciseLog, User, Exercise, Workout  

class UserExerciseLogCreate(BaseModel):
    exercise_id: int  
    workout_id: Optional[int] = None  
    set_number: int 
    reps: int  
    weight: Optional[float] = None  
    rest_seconds: Optional[int] = None
    duration_seconds: Optional[int] = None  
    distance_m: Optional[float] = None  
    volume: Optional[float] = None  
    notes: Optional[str] = None

class UserExerciseLogUpdate(BaseModel):
    reps: Optional[int] = None
    weight: Optional[float] = None
    rest_seconds: Optional[int] = None
    duration_seconds: Optional[int] = None
    distance_m: Optional[float] = None
    volume: Optional[float] = None
    notes: Optional[str] = None

class UserExerciseLogOut(BaseModel):
    id: int
    user_id: int
    exercise_id: int
    workout_id: Optional[int] = None
    date: datetime
    set_number: int
    reps: int
    weight: Optional[float] = None
    rest_seconds: Optional[int] = None
    duration_seconds: Optional[int] = None
    distance_m: Optional[float] = None
    volume: Optional[float] = None
    notes: Optional[str] = None
    created_at: datetime
    user: User  
    exercise: Exercise  
    workout: Optional[Workout] = None  

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True  # Pour relations

class AddLogsToWorkout(BaseModel):  # Body batch from localStorage
    logs: List[UserExerciseLogCreate]  # Array logs à push