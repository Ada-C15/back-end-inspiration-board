"""Add parent-child relationship

Revision ID: 993567e06e04
Revises: 5c91569e4771
Create Date: 2021-06-29 14:16:45.097471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '993567e06e04'
down_revision = '5c91569e4771'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card', sa.Column('board_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'card', 'board', ['board_id'], ['board_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'card', type_='foreignkey')
    op.drop_column('card', 'board_id')
    # ### end Alembic commands ###
