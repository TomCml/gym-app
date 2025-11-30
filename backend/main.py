import sys
import os
import logging  # Ajoute pour debug logs
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from app.database.config import settings
from app.routers.users import router as users_router
from app.routers.exercises import router as exercises_router
from app.routers.workouts import router as workouts_router
from app.routers import logs as logs_router
from app.routers import dashboard as dashboard_router

# Setup logging basique (sort dans Uvicorn logs)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(title=settings.PROJECT_NAME)

# Parsing safe : Default vide, try-except pour éviter crash
raw_origins = os.getenv("ALLOW_ORIGINS", "")
if not raw_origins:
    logger.warning("ALLOW_ORIGINS not set! Using fallback ['*'] for dev.")
    origins = ["*"]  # Fallback dev only (permissive, retire en prod)
else:
    origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    logger.info(f"CORS origins loaded: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],  # Bonus : Expose headers custom si besoin
)

# --------------------------------------------------------------------------

@app.get("/api")
def root():
    return {"message": "Server running"}

# Endpoint debug temporaire (supprime après)
@app.get("/debug-cors")
def debug_cors():
    return {
        "raw_allow_origins": os.getenv("ALLOW_ORIGINS", "NOT SET"),
        "parsed_origins": origins,
        "frontend_origin": "http://localhost:5173"  # À matcher
    }

app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(exercises_router, prefix="/api/exercises", tags=["exercises"])
app.include_router(workouts_router, prefix="/api/workouts", tags=["workouts"])
app.include_router(logs_router.router, prefix="/api/logs", tags=["logs"])
app.include_router(dashboard_router.router, prefix="/api/dashboard", tags=["dashboard"])