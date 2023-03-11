"""add last few columns to posts table

Revision ID: 9ed1c4a179b3
Revises: d503a8fd2083
Create Date: 2023-03-09 14:31:20.583963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ed1c4a179b3'
down_revision = 'd503a8fd2083'
branch_labels = None
depends_on = None


def upgrade():
    # addingg the last two columns into posts table.
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    pass


def downgrade():
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    pass
