"""Create table companies

Revision ID: 3194be78b6ae
Revises: 
Create Date: 2022-08-11 17:29:53.701886

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3194be78b6ae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'organisations',
        sa.Column('id', postgresql.UUID(), primary_key=True),
        sa.Column('name', sa.String())
    )


def downgrade() -> None:
    op.drop_table('organisations')


