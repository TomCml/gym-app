from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from ..models.base import Gender, ActivityLevel, Goal


class PasswordChange(BaseModel):
    current_password: str = Field(min_length=8, description="Current password")
    new_password: str = Field(
        min_length=8, description="New password must be at least 8 characters"
    )


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(
        min_length=8, description="Password must be at least 8 characters"
    )
    gender: Gender
    birthdate: datetime
    height_cm: int | None = None
    weight_kg: float | None = None
    body_fat_percentage: float | None = None
    activity_level: ActivityLevel | None = None
    goal: Goal | None = None


class UserUpdate(BaseModel):
    username: str
    email: EmailStr
    gender: Gender
    birthdate: datetime
    height_cm: int | None = None
    weight_kg: float | None = None
    body_fat_percentage: float | None = None
    activity_level: ActivityLevel | None = None
    goal: Goal | None = None


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    gender: Gender
    birthdate: datetime
    height_cm: int | None = None
    weight_kg: float | None = None
    body_fat_percentage: float | None = None
    activity_level: ActivityLevel | None = None
    goal: Goal | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserList(BaseModel):
    users: list[UserOut]
    total: int


class TokenData(BaseModel):
    user_id: int | None = None
