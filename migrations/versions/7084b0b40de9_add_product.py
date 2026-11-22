"""Add Product

Revision ID: 7084b0b40de9
Revises: 97fceb3466c3
Create Date: 2026-11-19 12:45:47.248704

"""
from alembic import op
import sqlalchemy as sa



revision = '7084b0b40de9'
down_revision = '97fceb3466c3'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )



def downgrade():

    op.drop_table('products')
