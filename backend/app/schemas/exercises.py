from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.base import Exercise, MuscleGroup, Difficulty


class ExerciseCreate(BaseModel):
    name: str
    description: Optional[str]
    muscle_group: MuscleGroup
    difficulty: Difficulty
    is_cardio: bool


class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    muscle_group: Optional[str] = None
    difficulty: Optional[str] = None
    is_cardio: Optional[bool] = None

class ExerciseOut(BaseModel):  
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    muscle_group: Optional[str] = None
    equipement: Optional[str] = None
    difficulty: Optional[str] = None
    is_cardio: bool = False  
    default_rest_seconds: Optional[int] = None  
    created_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True  

class ExerciseList(BaseModel):
    exercises: list[ExerciseOut]
    total: int