from typing import List, Optional, Tuple
from sqlmodel import select, func
from sqlalchemy.orm import Session
from datetime import datetime 
from app.database.db import get_session
from app.models.base import Workout, User  # User pour check FK
from app.schemas.workouts import WorkoutCreate, WorkoutUpdate, WorkoutOut
from .workout_exercises import WorkoutExerciseCreate
from app.models.base import Workout, WorkoutExercise, Exercise
from sqlmodel import select, delete
import logging  

def create_workout(workout_in: WorkoutCreate, session: Session) -> WorkoutOut:
    owner = session.get(User, workout_in.user_id)
    if not owner:
        raise ValueError("User not found")

    db_workout = Workout(
        name=workout_in.name,
        date=workout_in.date,
        notes=workout_in.notes,
        day_of_week=workout_in.day_of_week,
        user_id=workout_in.user_id
    )
    session.add(db_workout)
    session.commit()
    session.refresh(db_workout)  
    return WorkoutOut.model_validate(db_workout)

def get_workout(workout_id: int, session: Session) -> Optional[WorkoutOut]:
    workout = session.get(Workout, workout_id)
    if workout:
        return WorkoutOut.model_validate(workout)
    return None

def get_workouts(
    session: Session, offset: int, limit: int, user_id: Optional[int] = None
) -> Tuple[List[WorkoutOut], int]:
    
    count_statement = select(func.count(Workout.id))
    if user_id:
        count_statement = count_statement.where(Workout.user_id == user_id)
    
    total = session.exec(count_statement).one()

    data_statement = select(Workout).offset(offset).limit(limit)
    if user_id:
        data_statement = data_statement.where(Workout.user_id == user_id)

    workouts_db = session.exec(data_statement).all()
    
    workouts_out = [WorkoutOut.model_validate(w) for w in workouts_db]

    return workouts_out, total

def update_workout(workout_id: int, workout_update: WorkoutUpdate, session: Session) -> Optional[WorkoutOut]:
    db_workout = session.get(Workout, workout_id)
    if not db_workout:
        return None

    # On extrait les données du payload. exclude_unset=True est important.
    update_data = workout_update.model_dump(exclude_unset=True)

    # 1. Gérer la mise à jour des exercices, s'ils sont fournis
    if "exercises" in update_data:
        new_exercises_data = update_data.pop("exercises") # On les retire pour le traitement

        # a. Supprimer tous les anciens exercices liés à ce workout
        delete_statement = delete(WorkoutExercise).where(WorkoutExercise.workout_id == workout_id)
        session.exec(delete_statement)

        # b. Ajouter les nouveaux exercices
        for exercise_in in new_exercises_data:
            # On peut utiliser model_validate pour convertir le dict en Pydantic model si besoin
            ex_model = WorkoutExerciseCreate.model_validate(exercise_in)
            db_exercise = WorkoutExercise(
                workout_id=workout_id,
                **ex_model.model_dump()
            )
            session.add(db_exercise)

    # 2. Mettre à jour les champs simples du workout (name, notes, etc.)
    for key, value in update_data.items():
        setattr(db_workout, key, value)
    
    session.add(db_workout)
    session.commit()
    session.refresh(db_workout)
    
    return WorkoutOut.model_validate(db_workout)


def get_workout_for_day(user_id: int, day_of_week: int, session: Session) -> Optional[WorkoutOut]:
    workout_db = session.exec(
        select(Workout).where(Workout.user_id == user_id, Workout.day_of_week == day_of_week)
    ).first()
    
    if workout_db:
        return WorkoutOut.model_validate(workout_db)
    return None

def delete_workout(workout_id: int, session: Session) -> bool:
    workout = session.get(Workout, workout_id)
    if not workout:
        return False
    session.delete(workout)
    session.commit()
    return True


def create_default_workouts(db: Session, user_id: int):
    """
    Crée les 4 workouts de base pour un nouvel utilisateur.
    """
    
    all_exercises_query = db.exec(select(Exercise)).all()
    exercise_map = {ex.name: ex.id for ex in all_exercises_query}

    objects_to_add = [] 

    for workout_data in DEFAULT_WORKOUTS_DATA:
        new_workout = Workout(
            name=workout_data["name"],
            user_id=user_id
        )
        objects_to_add.append(new_workout)

        for ex_data in workout_data["exercises"]:
            ex_name = ex_data["name"]
            
            exercise_id = exercise_map.get(ex_name)
            
            if not exercise_id:
                logging.warning(f"Exercice de base '{ex_name}' non trouvé dans la BDD. Il ne sera pas ajouté au workout par défaut.")
                continue

            new_link = WorkoutExercise(
                workout=new_workout, 
                exercise_id=exercise_id,
                planned_sets=ex_data["sets"],
                planned_reps=ex_data["reps_str"],
                rest_seconds=ex_data["rest"],
                notes=ex_data["notes"]
            )
            objects_to_add.append(new_link)

    try:
        db.add_all(objects_to_add)
        db.commit()
        logging.info(f"Workouts de base créés avec succès pour l'utilisateur {user_id}")
    except Exception as e:
        db.rollback() 
        logging.error(f"Erreur lors de la création des workouts de base pour {user_id}: {e}")


DEFAULT_WORKOUTS_DATA = [
     
    {
        "name": "Push day",
        "exercises": [
            {"name": "Barbell Bench Press", "sets": 3, "reps_str": "7", "rest": 180, "notes": "RPE 8. Fundamental movement. Full body tension, drive through the feet."},
            {"name": "Incline Dumbbell Press", "sets": 3, "reps_str": "12", "rest": 120, "notes": "RPE 8.5. Focus on volume and hypertrophy."},
            {"name": "Cable Crossover", "sets": 3, "reps_str": "15", "rest": 90, "notes": "RPE 9. Endurance/Metabolic Hypertrophy."},
            {"name": "Dumbbell Lateral Raise", "sets": 3, "reps_str": "15", "rest": 60, "notes": "RPE 9. Isolate the medial deltoid. Strict movement."},
            {"name": "Reverse Grip Triceps Pushdown", "sets": 3, "reps_str": "15", "rest": 60, "notes": "RPE 9. Focus on full extension."}, 
            {"name": "Face Pull", "sets": 2, "reps_str": "20", "rest": 60, "notes": "RPE 7. Rotator cuff and rear delt work."},
        ]
    },
    {
        "name": "Pull day",
        "exercises": [
            {"name": "Pull-up", "sets": 3, "reps_str": "7", "rest": 180, "notes": "RPE 8. Back/Strength Priority. Initiate with scapulae."},
            {"name": "Romanian Deadlift (RDL)", "sets": 3, "reps_str": "10", "rest": 150, "notes": "RPE 8. Push hips back, maintain neutral spine."},
            {"name": "Bent-Over Barbell Row", "sets": 3, "reps_str": "12", "rest": 120, "notes": "RPE 8.5. Pull with the elbows. Contract mid-back."},
            {"name": "Seated Cable Row", "sets": 3, "reps_str": "115", "rest": 90, "notes": "RPE 9. Back Endurance/Hypertrophy."},
            {"name": "Standing Barbell Curl", "sets": 3, "reps_str": "15", "rest": 60, "notes": "RPE 9. Strict control, no swinging."},
            {"name": "Hammer Curl", "sets": 2, "reps_str": "15", "rest": 60, "notes": "RPE 8. For arm thickness."},
        ]
    },
    {
        "name": "Insane leg day",
        "exercises": [
            {"name": "Barbell Back Squat", "sets": 3, "reps_str": "7", "rest": 180, "notes": "RPE 8. Strength Priority. Impeccable technique."},
            {"name": "Leg Press", "sets": 3, "reps_str": "12", "rest": 120, "notes": "RPE 8.5. Hypertrophy. Control the range of motion."},
            {"name": "Reverse Lunge", "sets": 3, "reps_str": "15", "rest": 90, "notes": "RPE 9. Stability and balance. Aim for a long step."},
            {"name": "Leg Extension", "sets": 3, "reps_str": "20", "rest": 60, "notes": "RPE 9.5. Endurance. Hold peak contraction 1-2s."},
            {"name": "Seated Leg Curl", "sets": 3, "reps_str": "15", "rest": 60, "notes": "RPE 9. Hamstring focus. Mind-muscle connection."},
            {"name": "Standing Calf Raise", "sets": 3, "reps_str": "20", "rest": 60, "notes": "RPE 9.5. Maximal range of motion."},
        ]
    },
    {
        "name": "Full body",
        "exercises": [
            {"name": "Hack Squat", "sets": 2, "reps_str": "20", "rest": 90, "notes": "RPE 7.5. Light load. Controlled but quick tempo."},
            {"name": "Lat Pulldown", "sets": 2, "reps_str": "20", "rest": 60, "notes": "RPE 7.5. Focus on tempo and feel."},
            {"name": "Push-up", "sets": 2, "reps_str": "20", "rest": 60, "notes": "RPE 7.5. Focus on explosive pushing."},
            {"name": "Walking Lunge", "sets": 2, "reps_str": "20", "rest": 60, "notes": "RPE 7. Mobility and endurance."},
            {"name": "Standing Barbell Curl", "sets": 2, "reps_str": "15", "rest": 45, "notes": "RPE 7. Light "}, 
        ]
    },
]