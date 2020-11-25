"""Upgrade Reading and Sensor

Revision ID: 90cdd6bb4e97
Revises: 196b807a9eee
Create Date: 2020-11-24 22:59:54.216597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90cdd6bb4e97'
down_revision = '196b807a9eee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Users')
    op.drop_index('ix_Readings_timestamp', table_name='Readings')
    op.drop_table('Readings')
    op.drop_table('association')
    op.drop_table('Sensors')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Sensors',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association',
    sa.Column('Users_id', sa.INTEGER(), nullable=True),
    sa.Column('Sensors_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['Sensors_id'], ['Sensors.id'], ),
    sa.ForeignKeyConstraint(['Users_id'], ['Users.id'], )
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