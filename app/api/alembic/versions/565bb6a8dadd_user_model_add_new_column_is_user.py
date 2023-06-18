"""user model add new column is_user

Revision ID: 565bb6a8dadd
Revises: 3ccc68bacbe7
Create Date: 2023-06-14 16:31:57.871306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '565bb6a8dadd'
down_revision = '3ccc68bacbe7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_user', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_user')
    # ### end Alembic commands ###
