"""added date_time column

Revision ID: 1b15a51f98c5
Revises: c579c6ad9e26
Create Date: 2020-07-22 13:01:59.002863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b15a51f98c5'
down_revision = 'c579c6ad9e26'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('date_time', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'date_time')
    # ### end Alembic commands ###
