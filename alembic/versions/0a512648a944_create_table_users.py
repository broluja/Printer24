"""Create table users

Revision ID: 0a512648a944
Revises: 3194be78b6ae
Create Date: 2022-08-11 17:33:26.204514

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0a512648a944'
down_revision = '3194be78b6ae'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(), primary_key=True),
        sa.Column('first_name', sa.String()),
        sa.Column('last_name', sa.String()),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('company', postgresql.UUID(), sa.ForeignKey('organisations.id')),
        sa.Column('hashed_password', sa.String(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.Column('has_color', sa.Boolean(), nullable=True),
        sa.Column('limit', sa.Integer(), default=50),
        sa.Column('code', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_user_email'), 'users', ['email'], unique=True)


def downgrade() -> None:
    op.drop_table('users')
