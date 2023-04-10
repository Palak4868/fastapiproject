"""add foreign-key to posts table

Revision ID: 5a8a6f956f8f
Revises: 58ef7d762360
Create Date: 2023-04-10 13:00:17.706537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a8a6f956f8f'
down_revision = '58ef7d762360'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key("post_users_fk", "posts", "users", ['owner_id'], ['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts','owner_id')
    pass
