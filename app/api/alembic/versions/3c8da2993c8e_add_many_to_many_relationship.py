"""add many to many relationship

Revision ID: 3c8da2993c8e
Revises: 0aae46d26763
Create Date: 2023-06-27 09:30:04.822048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c8da2993c8e'
down_revision = '0aae46d26763'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ordered_products', sa.Column('product_id', sa.Integer(), nullable=True))
    op.add_column('ordered_products', sa.Column('order_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'ordered_products', 'products', ['product_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'ordered_products', 'orders', ['order_id'], ['id'], ondelete='CASCADE')
    op.add_column('orders', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'orders', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_column('orders', 'user_id')
    op.drop_constraint(None, 'ordered_products', type_='foreignkey')
    op.drop_constraint(None, 'ordered_products', type_='foreignkey')
    op.drop_column('ordered_products', 'order_id')
    op.drop_column('ordered_products', 'product_id')
    # ### end Alembic commands ###
