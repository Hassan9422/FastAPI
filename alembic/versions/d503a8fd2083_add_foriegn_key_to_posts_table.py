"""add foriegn_key to posts table

Revision ID: d503a8fd2083
Revises: 73e2283c9e68
Create Date: 2023-03-09 14:13:06.629996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd503a8fd2083'
down_revision = '73e2283c9e68'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fkey', source_table='posts', referent_table='users',
                           local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fkey", 'posts')
    op.drop_column("posts", "owner_id")
    pass
