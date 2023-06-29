"""ordered product update

Revision ID: 10c4369fc4af
Revises: 59faab78cf33
Create Date: 2023-06-29 14:41:07.845037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10c4369fc4af'
down_revision = '59faab78cf33'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ordered_products', 'count')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ordered_products', sa.Column('count', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###