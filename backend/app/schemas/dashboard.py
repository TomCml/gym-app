from pydantic import BaseModel
from typing import Optional
from .workouts import WorkoutOut

class DashboardData(BaseModel):
    todays_workout: Optional[WorkoutOut] = None
    yesterday_skipped: bool = False