from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Import your settings
from app.database.config import settings

# Import SQLModel (this is your "Base")
from sqlmodel import SQLModel

# IMPORTANT: Import all your models here so Alembic can detect them
# Adjust these imports based on your actual model locations
try:
    from app.models.base import User
    from app.schemas.exercises import Exercise
    from app.schemas.user_exercise_log import UserExerciseLog
    from app.schemas.workouts import Workout
    from app.schemas.workout_exercises import WorkoutExercise
    from app.schemas.dashboard import DashboardData
    
    # Add any other models you have
except ImportError as e:
    print(f"Warning: Could not import some models: {e}")

config = context.config

# Override the sqlalchemy.url with your settings
config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URI)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use SQLModel.metadata instead of Base.metadata
target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.SQLALCHEMY_DATABASE_URI
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = settings.SQLALCHEMY_DATABASE_URI
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()