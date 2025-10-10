import sys
import os
from fastapi import FastAPI
from app.database.config import settings
from app.routers.users import router as users_router
from app.routers.exercises import router as exercises_router
from app.routers.workouts import router as workouts_router
sys.path.append(os.path.dirname(os.path.abspath(__file__)))



app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/api")
def root():
    return {"message": "Server running"}

app.include_router(users_router, prefix="/api/users", tags=["users"])  


app.include_router(exercises_router, prefix="/api/exercises", tags=["exercises"])


app.include_router(workouts_router, prefix="/api/workouts", tags=["workouts"])

