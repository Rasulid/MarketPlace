"""add category fk

Revision ID: 503327c84eb8
Revises: a50ada407acb
Create Date: 2023-07-02 12:19:43.290794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '503327c84eb8'
down_revision = 'a50ada407acb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('products', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'products', 'category', ['category_id'], ['id'], ondelete='SET NULL')
    op.drop_column('products', 'category')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('category', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.drop_column('products', 'category_id')
    op.drop_table('category')
    # ### end Alembic commands ###