"""initial migration

Revision ID: 7b47a5b3039b
Revises: cf3f24aa178c
Create Date: 2024-03-25 21:40:09.387727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b47a5b3039b'
down_revision: Union[str, None] = 'cf3f24aa178c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
