"""Add a column

Revision ID: 73926dc3cceb
Revises: d4b727ba1c33
Create Date: 2022-08-11 10:02:34.274059

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '73926dc3cceb'
down_revision = 'd4b727ba1c33'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('company', postgresql.UUID(), sa.ForeignKey('organisations.id')),)


def downgrade() -> None:
    op.drop_column('users', 'company')
