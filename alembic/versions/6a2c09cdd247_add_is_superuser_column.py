"""add is_superuser column

Revision ID: 6a2c09cdd247
Revises: 7b47a5b3039b
Create Date: 2024-03-25 21:49:51.035681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a2c09cdd247'
down_revision: Union[str, None] = '7b47a5b3039b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
