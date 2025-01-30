"""email

Revision ID: 275033913bcf
Revises: 23981dec89ad
Create Date: 2025-01-30 14:31:36.258581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '275033913bcf'
down_revision: Union[str, None] = '23981dec89ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
