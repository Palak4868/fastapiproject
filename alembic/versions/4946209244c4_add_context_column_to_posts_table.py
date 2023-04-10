"""add context column to posts table

Revision ID: 4946209244c4
Revises: e893a4c4534f
Create Date: 2023-04-08 20:43:41.002648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4946209244c4'
down_revision = 'e893a4c4534f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
