"""add content column in posts

Revision ID: dda7eafb48b8
Revises: 51e5c3f2673e
Create Date: 2023-03-08 17:13:43.931195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dda7eafb48b8'
down_revision = '51e5c3f2673e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')

