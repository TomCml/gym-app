from enum import Enum  
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List 

#USERS
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
    username: str = Field(sa_column_kwargs={"nullable": False, "unique": True})
    email: str = Field(sa_column_kwargs={"nullable": False, "unique": True})
    hashed_password: str = Field(sa_column_kwargs={"nullable": False})
    gender: Optional[str] = None
    birthdate: Optional[datetime] = None
    height_cm: Optional[int] = None
    weight_kg: Optional[float] = None
    body_fat: Optional[float] = None
    activity_level: Optional[str] = None
    goal: Optional[str] = None
    created_at: datetime = Field(sa_column_kwargs={"server_default": "now()"})
    updated_at: datetime = Field(sa_column_kwargs={"server_default": "now()", "onupdate": "now()"})

    # Relations
    workouts: List["Workout"] = Relationship(back_populates="user")
    logs: List["UserExerciseLog"] = Relationship(back_populates="user")

#EXERCICES
class GymEquipment(str, Enum):
    AB_WHEEL = "Ab wheel (roue abdominale)"
    AIR_BIKE = "Air bike (vélo à résistance à air)"
    BARRE_DE_TRACTION = "Barre de traction"
    BARRE_EZ = "Barre EZ"
    BARRE_OLYMPIQUE = "Barre olympique"
    BANC_DE_MUSCULATION = "Banc de musculation"
    BATTLE_ROPE = "Battle rope (corde ondulatoire)"
    BOX_PLYOMETRIE = "Box de pliométrie"
    CORDE_A_SAUTER = "Corde à sauter"
    CORDE_ESCALADE = "Corde d’escalade"
    DISQUES_MUSCULATION = "Disques de musculation (poids)"
    ELASTIQUES_RESISTANCE = "Élastiques de résistance"
    GILET_LESTE = "Gilet lesté"
    HALTERES = "Haltères"
    KETTLEBELL = "Kettlebell"
    LEG_CURL = "Leg curl (ischios)"
    LEG_EXTENSION = "Leg extension (quadriceps)"
    LEG_PRESS = "Leg press (presse à cuisses)"
    MACHINE_ADDUCTEURS_ABDUCTEURS = "Machine à adducteurs/abducteurs"
    MACHINE_DIPS_ASSISTEES = "Machine à dips/tractions assistées"
    MACHINE_FESSIERS = "Machine à fessiers"
    MACHINE_POULIE = "Machine à poulie (câble)"
    MEDECINE_BALL = "Medecine ball (balle lestée)"
    RACK_SQUAT = "Rack à squat"
    RAMEUR = "Rameur"
    SMITH_MACHINE = "Smith machine (cadre guidé)"
    STEPPER = "Stepper"
    TAPIS_DE_COURSE = "Tapis de course"
    VELO_ELLIPTIQUE = "Vélo elliptique"

class MuscleGroup(str, Enum):
    # Haut du corps
    PECTORAUX = "Pectoraux (grand pectoral, pectoral inférieur, pectoral supérieur)"
    DOS = "Dos (grand dorsal, trapèzes, rhomboïdes)"
    EPAULES = "Épaules / Deltoïdes (antérieur, moyen, postérieur)"
    BICEPS = "Biceps (biceps brachial, brachial antérieur)"
    TRICEPS = "Triceps (chef long, latéral et médial)"
    AVANT_BRAS = "Avant-bras (fléchisseurs, extenseurs, pronateurs, supinateurs)"
    
    # Tronc
    ABDOMINAUX = "Abdominaux (grand droit, transverse)"
    OBLIQUES = "Obliques (internes et externes)"
    LOMBAIRES = "Lombaires (muscles érecteurs du rachis)"
    
    # Bas du corps
    FESSIERS = "Fessiers (grand, moyen et petit fessier)"
    QUADRICEPS = "Quadriceps (vaste médial, latéral, droit fémoral)"
    ISCHIO_JAMBIERS = "Ischio-jambiers (biceps fémoral, semi-tendineux, semi-membraneux)"
    ADDUCTEURS = "Adducteurs (grand adducteur, long adducteur, pectiné)"
    ABDUCTEURS = "Abducteurs (tenseur du fascia lata, moyen fessier)"
    MOLLETS = "Mollets (gastrocnémien, soléaire)"
    
    # Autres
    COU = "Cou (sternocléidomastoïdien, muscles cervicaux)"
    CARDIO = "Cardio / Endurance (système cardiovasculaire)"

class Difficulty(str, Enum):
    BEGINNER_FRIENDLY = "beginner friendly"
    EASY = "easy"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    ELITE = "elite"

class Exercise(SQLModel, table=True):
    __tablename__ = "exercises"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, sa_column_kwargs={"unique": True})
    description: Optional[str] = None
    muscle_group: Optional[str] = None
    equipement: Optional[str] = None
    difficulty: Optional[str] = None
    is_cardio: bool = False
    default_rest_seconds: Optional[int] = None  # Ajouté du dump
    created_at: datetime = Field(sa_column_kwargs={"server_default": "now()"})

    # Relations
    workout_exercises: List["WorkoutExercise"] = Relationship(back_populates="exercise")
    logs: List["UserExerciseLog"] = Relationship(back_populates="exercise")

class Workout(SQLModel, table=True):
    __tablename__ = "workouts"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id") 
    name: str = Field(sa_column_kwargs={"nullable": False})
    date: datetime = Field(sa_column_kwargs={"server_default": "now()"})
    notes: Optional[str] = None
    day_of_week: Optional[str] = None

    # Relations
    user: "User" = Relationship(back_populates="workouts")
    workout_exercises: List["WorkoutExercise"] = Relationship(
        back_populates="workout",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    logs: List["UserExerciseLog"] = Relationship(
        back_populates="workout",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class WorkoutExercise(SQLModel, table=True):
    __tablename__ = "workout_exercises"
    id: Optional[int] = Field(default=None, primary_key=True)
    workout_id: int = Field(foreign_key="workouts.id", ondelete="CASCADE")
    exercise_id: int = Field(foreign_key="exercises.id")
    planned_sets: Optional[int] = None
    planned_reps: Optional[int] = None
    planned_weight: Optional[float] = None  
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None

    # Relations
    workout: "Workout" = Relationship(back_populates="workout_exercises")
    exercise: "Exercise" = Relationship(back_populates="workout_exercises")

class UserExerciseLog(SQLModel, table=True):
    __tablename__ = "user_exercise_logs"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE")
    exercise_id: int = Field(foreign_key="exercises.id")
    workout_id: Optional[int] = Field(foreign_key="workouts.id", ondelete="CASCADE")
    date: datetime = Field(sa_column_kwargs={"nullable": False, "server_default": "now()"})
    set_number: int = Field(sa_column_kwargs={"nullable": False})
    reps: int = Field(sa_column_kwargs={"nullable": False})
    weight: Optional[float] = None  # numeric(6,2)
    rest_seconds: Optional[int] = None
    duration_seconds: Optional[int] = None
    distance_m: Optional[float] = None  # numeric(8,2)
    volume: Optional[float] = None  # numeric(10,2)
    created_at: datetime = Field(sa_column_kwargs={"server_default": "now()"})

    # Relations
    user: "User" = Relationship(back_populates="logs")
    exercise: "Exercise" = Relationship(back_populates="logs")
    workout: Optional["Workout"] = Relationship(back_populates="logs")