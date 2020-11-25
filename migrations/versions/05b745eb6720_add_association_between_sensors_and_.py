"""Add association between Sensors and Users

Revision ID: 05b745eb6720
Revises: 2bc0e3089b08
Create Date: 2020-11-24 18:46:31.011301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05b745eb6720'
down_revision = '2bc0e3089b08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Users')
    op.drop_index('ix_Readings_timestamp', table_name='Readings')
    op.drop_table('Readings')
    op.drop_table('Sensors')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Sensors',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Readings',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('value', sa.VARCHAR(length=30), nullable=True),
    sa.Column('unit', sa.VARCHAR(length=5), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('sensor_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['sensor_id'], ['Sensors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_Readings_timestamp', 'Readings', ['timestamp'], unique=False)
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
