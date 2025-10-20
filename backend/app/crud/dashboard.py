from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.crud.workouts import get_workout_for_day
from app.crud.user_exercise_log import get_logs_for_date
from app.schemas.dashboard import DashboardData

def get_dashboard_data(user_id: int, session: Session) -> DashboardData:
    today = date.today()
    yesterday = today - timedelta(days=1)

    # 1. Récupérer l'entraînement du jour
    todays_workout = get_workout_for_day(user_id=user_id, day_of_week=today.isoweekday(), session=session)

    # 2. Vérifier si l'entraînement d'hier a été "skip"
    yesterday_skipped = False
    yesterdays_plan = get_workout_for_day(user_id=user_id, day_of_week=yesterday.isoweekday(), session=session)
    
    if yesterdays_plan:
        yesterdays_logs = get_logs_for_date(user_id=user_id, target_date=yesterday, session=session)
        if not yesterdays_logs:
            yesterday_skipped = True

    return DashboardData(
        todays_workout=todays_workout,
        yesterday_skipped=yesterday_skipped
    )