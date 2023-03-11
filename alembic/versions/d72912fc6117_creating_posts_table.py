"""creating posts table

Revision ID: d72912fc6117
Revises: 
Create Date: 2023-03-09 12:50:50.212434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd72912fc6117'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False))
    pass


# and this function is for rolling back to a previous step or state in database.
def downgrade():

    op.drop_table('posts')
    pass
