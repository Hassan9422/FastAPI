"""adding content column to posts table

Revision ID: 973a1fdbb85a
Revises: d72912fc6117
Create Date: 2023-03-09 12:54:17.474417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '973a1fdbb85a'
down_revision = 'd72912fc6117'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
