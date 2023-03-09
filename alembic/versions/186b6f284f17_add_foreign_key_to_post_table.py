"""add foreign key to post table

Revision ID: 186b6f284f17
Revises: ed499ea60441
Create Date: 2023-03-08 17:31:54.782280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '186b6f284f17'
down_revision = 'ed499ea60441'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'],
                          remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
