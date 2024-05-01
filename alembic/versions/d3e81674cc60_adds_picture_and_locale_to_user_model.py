"""adds picture and locale to user model

Revision ID: d3e81674cc60
Revises: 39e9524b7803
Create Date: 2024-04-28 11:28:12.306888

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3e81674cc60'
down_revision: Union[str, None] = '39e9524b7803'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('picture', sa.String(), nullable=True))
    op.add_column('users', sa.Column('locale', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'picture')
    op.drop_column('users', 'locale')
