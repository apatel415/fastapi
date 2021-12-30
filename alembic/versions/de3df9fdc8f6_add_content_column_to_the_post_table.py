"""add content column to the post table

Revision ID: de3df9fdc8f6
Revises: 243dffc369e0
Create Date: 2021-12-29 22:58:24.306101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de3df9fdc8f6'
down_revision = '243dffc369e0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
