from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_session
from app.crud import dashboard as crud_dashboard
from app.schemas.dashboard import DashboardData

router = APIRouter()

@router.get("/{user_id}", response_model=DashboardData)
def get_user_dashboard(user_id: int, session: Session = Depends(get_session)):
    return crud_dashboard.get_dashboard_data(user_id=user_id, session=session)