"""add is_admin column

Revision ID: d0619a0315f7
Revises: 6a2c09cdd247
Create Date: 2024-03-25 21:55:04.009453

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0619a0315f7'
down_revision: Union[str, None] = '6a2c09cdd247'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
