"""Add unaccent extension

Revision ID: b4ce7c83e53a
Revises: c31b2bb628f2
Create Date: 2025-10-27 19:30:51.970178

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = 'b4ce7c83e53a'
down_revision: Union[str, None] = 'c31b2bb628f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.execute("CREATE EXTENSION IF NOT EXISTS unaccent")
    


def downgrade() -> None:
    
    op.execute("DROP EXTENSION IF EXISTS unaccent")