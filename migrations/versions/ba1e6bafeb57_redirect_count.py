"""redirect count

Revision ID: ba1e6bafeb57
Revises: c3acab244902
Create Date: 2024-05-28 20:47:58.447484

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ba1e6bafeb57'
down_revision: Union[str, None] = 'c3acab244902'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('short_url', sa.Column('redirect_count', sa.INTEGER(), default=0))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('short_url', 'redirect_count')
    # ### end Alembic commands ###