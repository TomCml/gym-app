from typing import Optional
from enum import Enum  
from sqlmodel import SQLModel, Field
from datetime import datetime

class Gender(str, Enum):
    MALE = "male" 
    FEMALE = "female" 

class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    ACTIVE = "active"
    ATHLETE = "athlete"

class Goal(str, Enum):
    LOSE_WEIGHT = "lose_weight"
    GAIN_MUSCLE = "gain_muscle"
    MAINTAIN = "maintain"
    IMPROVE_FITNESS = "improve_fitness"

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, max_length=50) 
    email: str = Field(index=True, unique=True, sa_column_kwargs={"nullable": False})  
    hashed_password: str = Field(sa_column_kwargs={"nullable": False}) 
    gender: Gender  
    birthdate: datetime  
    height_cm: Optional[int] = Field(default=None, ge=50, le=250)  
    weight_kg: Optional[float] = Field(default=None, ge=30, le=300)  
    body_fat: Optional[float] = Field(default=None, ge=0, le=100)  
    activity_level: ActivityLevel
    goal: Goal
    created_at: datetime = Field(default_factory=datetime.utcnow)  
    updated_at: datetime = Field(
        sa_column_kwargs={
            "server_default": "now()",  
            "onupdate": "now()"  
        }
    )