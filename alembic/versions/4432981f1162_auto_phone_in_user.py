"""auto phone in user

Revision ID: 4432981f1162
Revises: dfb63eb7b23f
Create Date: 2021-12-30 07:01:27.303723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4432981f1162'
down_revision = 'dfb63eb7b23f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
