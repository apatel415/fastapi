"""add remaining columns

Revision ID: a0af3016f8bf
Revises: b23fe15eaa38
Create Date: 2021-12-29 23:22:16.208533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0af3016f8bf'
down_revision = 'b23fe15eaa38'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
