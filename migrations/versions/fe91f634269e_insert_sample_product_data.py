"""Insert sample product data

Revision ID: fe91f634269e
Revises: fc7f390f4c06
Create Date: 2026-11-19 12:50:13.341182

"""
from alembic import op
import sqlalchemy as sa



revision = 'fe91f634269e'
down_revision = 'fc7f390f4c06'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        sa.text(
            "INSERT OR IGNORE INTO categories (name) "
            "VALUES ('Migration samples')"
        )
    )
    op.execute(
        sa.text(
            "INSERT INTO products (name, price, active, category_id, created_at) "
            "SELECT 'Migration sample product', 125.50, 1, categories.id, "
            "CURRENT_TIMESTAMP FROM categories "
            "WHERE categories.name = 'Migration samples' "
            "AND NOT EXISTS (SELECT 1 FROM products "
            "WHERE name = 'Migration sample product')"
        )
    )


def downgrade():
    op.execute(
        sa.text("DELETE FROM products WHERE name = 'Migration sample product'")
    )
    op.execute(
        sa.text(
            "DELETE FROM categories WHERE name = 'Migration samples' "
            "AND NOT EXISTS (SELECT 1 FROM products "
            "WHERE products.category_id = categories.id)"
        )
    )
