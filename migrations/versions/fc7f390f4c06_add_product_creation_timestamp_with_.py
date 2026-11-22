"""Add product creation timestamp with database default

Revision ID: fc7f390f4c06
Revises: 277ca243e721
Create Date: 2026-11-19 12:50:02.242089

"""
from alembic import op
import sqlalchemy as sa



revision = 'fc7f390f4c06'
down_revision = '277ca243e721'
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))




def downgrade():

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('created_at')
