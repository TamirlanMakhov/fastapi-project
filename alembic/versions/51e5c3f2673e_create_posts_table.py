"""create posts table

Revision ID: 51e5c3f2673e
Revises: 
Create Date: 2023-03-08 16:57:01.331813

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '51e5c3f2673e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String, nullable=False, ))



def downgrade() -> None:
    op.drop_table('posts')

