from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.base import Workout, User, WorkoutExercise, Exercise  # Relations

class WorkoutCreate(BaseModel):
    name: str
    date: Optional[datetime] = None
    notes: Optional[str] = None
    user_id: int  

class WorkoutUpdate(BaseModel):
    name: Optional[str] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None

class WorkoutOut(BaseModel):
    id: int
    name: str
    date: datetime
    notes: Optional[str]
    user_id: int
    user: User  
    workout_exercises: List[WorkoutExercise]  

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class WorkoutList(BaseModel):
    workouts: List[WorkoutOut]
    total: int