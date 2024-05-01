"""cpf optional

Revision ID: 39e9524b7803
Revises: f709e9b0d5cc
Create Date: 2024-04-28 11:07:35.529125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39e9524b7803'
down_revision: Union[str, None] = 'f709e9b0d5cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
