"""initial migration

Revision ID: cf3f24aa178c
Revises: 10696f0a5531
Create Date: 2024-03-25 21:31:48.964060

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf3f24aa178c'
down_revision: Union[str, None] = '10696f0a5531'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
