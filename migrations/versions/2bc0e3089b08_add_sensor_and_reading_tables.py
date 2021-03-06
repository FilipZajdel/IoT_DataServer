"""Add Sensor and Reading tables

Revision ID: 2bc0e3089b08
Revises: 87dbea3c75e6
Create Date: 2020-11-24 18:36:44.765092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bc0e3089b08'
down_revision = '87dbea3c75e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=120), nullable=True),
    sa.Column('email', sa.VARCHAR(length=120), nullable=True),
    sa.Column('priviledged', sa.BOOLEAN(), nullable=True),
    sa.Column('password', sa.VARCHAR(length=30), nullable=True),
    sa.CheckConstraint('priviledged IN (0, 1)'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('priviledged')
    )
    # ### end Alembic commands ###
