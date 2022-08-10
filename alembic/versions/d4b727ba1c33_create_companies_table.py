"""Create companies table

Revision ID: d4b727ba1c33
Revises: 783730c4b401
Create Date: 2022-08-10 22:33:59.260303

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd4b727ba1c33'
down_revision = '783730c4b401'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'organisations',
        sa.Column('id', postgresql.UUID(), primary_key=True),
        sa.Column('organisation', sa.String())
    )


def downgrade() -> None:
    op.drop_table('organisations')
