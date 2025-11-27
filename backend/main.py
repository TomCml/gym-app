import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from app.database.config import settings
from app.routers.users import router as users_router
from app.routers.exercises import router as exercises_router
from app.routers.workouts import router as workouts_router
from app.routers import logs as logs_router
from app.routers import dashboard as dashboard_router

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(title=settings.PROJECT_NAME)

frontend_url = os.getenv("ALLOW_ORIGIN", "http://localhost:5173")
print(f"--- INFO: Autorisation CORS pour l'origine: {frontend_url} ---") # Pour déboguer

# --------------------------------------------------------------------------
# CORRECTION ICI : Utilisez de vrais espaces pour l'indentation
origins = [
    frontend_url, 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Autorise les origines listées
    allow_credentials=True,      # Autorise les cookies et en-têtes d'authentification
    allow_methods=["*"],         # Autorise toutes les méthodes (POST, GET, etc.)
    allow_headers=["*"],         # Autorise tous les en-têtes
)
# --------------------------------------------------------------------------

@app.get("/api")
def root():
    # CORRECTION ICI : Utilisez de vrais espaces
    return {"message": "Server running"}

app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(exercises_router, prefix="/api/exercises", tags=["exercises"])
app.include_router(workouts_router, prefix="/api/workouts", tags=["workouts"])
app.include_router(logs_router.router, prefix="/api/logs", tags=["logs"])
app.include_router(dashboard_router.router, prefix="/api/dashboard", tags=["dashboard"])