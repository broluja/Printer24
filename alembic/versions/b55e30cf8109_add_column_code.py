"""Add column code

Revision ID: b55e30cf8109
Revises: 73926dc3cceb
Create Date: 2022-08-11 13:42:07.371196

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b55e30cf8109'
down_revision = '73926dc3cceb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('code', sa.Integer, nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'code')
