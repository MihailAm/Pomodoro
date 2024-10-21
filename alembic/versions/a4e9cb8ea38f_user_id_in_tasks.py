"""user_id_in_tasks

Revision ID: a4e9cb8ea38f
Revises: e177248db47b
Create Date: 2024-10-21 15:11:44.065984

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4e9cb8ea38f'
down_revision: Union[str, None] = 'e177248db47b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Tasks', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'Tasks', 'UserProfile', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Tasks', type_='foreignkey')
    op.drop_column('Tasks', 'user_id')
    # ### end Alembic commands ###
