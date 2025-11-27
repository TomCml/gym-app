"""Seed exercises data

Revision ID: b448a8abf505
Revises: b4ce7c83e53a
Create Date: 2025-10-27 20:02:19.819072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import os

# revision identifiers, used by Alembic.
revision: str = 'b448a8abf505'
down_revision: Union[str, None] = 'b4ce7c83e53a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sql_file_path = 'seed_exercises.sql'
    with open(sql_file_path, 'r') as f:
        sql_content = f.read()

    op.execute(sql_content)


def downgrade() -> None:
    op.execute("TRUNCATE TABLE exercises RESTART IDENTITY CASCADE")
