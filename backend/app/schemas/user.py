from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum 
from datetime import datetime
from app.models.base import Gender, ActivityLevel, Goal  

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8, description="Password must be at least 8 characters")
    gender: Gender
    birthdate: datetime
    height_cm: Optional[Optional[int]]= None
    weight_kg: Optional[Optional[float]] = None
    body_fat_percentage: Optional[Optional[float]] = None
    activity_level: Optional[Optional[ActivityLevel]] = None
    goal: Optional[Optional[Goal]]= None

class UserUpdate(BaseModel):
    username: str
    email: EmailStr
    gender: Gender
    birthdate: datetime
    height_cm: Optional[Optional[int]]= None
    weight_kg: Optional[Optional[float]] = None
    body_fat_percentage: Optional[Optional[float]] = None
    activity_level: Optional[Optional[ActivityLevel]] = None
    goal: Optional[Optional[Goal]]= None

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    gender: Gender
    birthdate: datetime
    height_cm: Optional[int]
    weight_kg: Optional[float]
    body_fat_percentage: Optional[float]
    activity_level: ActivityLevel
    goal: Goal
    created_at: datetime
    updated_at: datetime

class Config:
    from_attributes = True

class UserList(BaseModel):
    users: list[UserOut]
    total: int