"""add user table

Revision ID: 58ef7d762360
Revises: 4946209244c4
Create Date: 2023-04-08 20:57:42.331722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58ef7d762360'
down_revision = '4946209244c4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',sa.Column('id', sa.Integer(), nullable=False), sa.Column('email', sa.String(), nullable=False),sa.Column('password', sa.String(), nullable=False), sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email'))

    pass


def downgrade():
    op.drop_table('users')
    pass
