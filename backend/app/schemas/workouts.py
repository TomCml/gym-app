from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.base import Workout, WorkoutExercise, Exercise
from app.schemas.user import UserOut
from app.schemas.workout_exercises import WorkoutExerciseOut, WorkoutExerciseCreate

class WorkoutCreate(BaseModel):
    name: str
    date: Optional[datetime] = None
    notes: Optional[str] = None
    day_of_week: Optional[int] = None
    user_id: int  

class WorkoutUpdate(BaseModel):
    name: Optional[str] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None
    day_of_week: Optional[int] = None

    exercises: Optional[List[WorkoutExerciseCreate]] = None


class WorkoutOut(BaseModel):
    id: int
    name: str
    date: datetime
    notes: Optional[str]
    day_of_week: Optional[int] = None
    user_id: int
    user: UserOut
    workout_exercises: List[WorkoutExerciseOut]  

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class WorkoutList(BaseModel):
    workouts: List[WorkoutOut]
    total: int