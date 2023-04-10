"""create posts table

Revision ID: e893a4c4534f
Revises: 
Create Date: 2023-04-08 20:05:25.376654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e893a4c4534f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id', sa.Integer(),nullable=False, primary_key=True), sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
