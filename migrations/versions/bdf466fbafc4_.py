"""empty message

Revision ID: bdf466fbafc4
Revises: 94b75ad2c490
Create Date: 2020-12-14 17:15:05.807737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdf466fbafc4'
down_revision = '94b75ad2c490'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('room', sa.Column('description', sa.String(length=100), nullable=True))
    op.add_column('room', sa.Column('location', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('room', 'location')
    op.drop_column('room', 'description')
    # ### end Alembic commands ###
