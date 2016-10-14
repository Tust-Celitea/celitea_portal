"""registration

Revision ID: ef2b9eb53718
Revises: 678fd7ac08f0
Create Date: 2016-10-14 19:02:40.719489

"""

# revision identifiers, used by Alembic.
revision = 'ef2b9eb53718'
down_revision = '678fd7ac08f0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('registration',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('classnum', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('ablity', sa.Text(), nullable=True),
    sa.Column('desc', sa.Text(), nullable=True),
    sa.Column('phone', sa.String(length=64), nullable=True),
    sa.Column('qq', sa.String(length=64), nullable=True),
    sa.Column('photo', sa.String(length=32), nullable=True),
    sa.Column('wechat', sa.String(length=64), nullable=True),
    sa.Column('telegram', sa.String(length=64), nullable=True),
    sa.Column('personal_page', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_registration_email'), 'registration', ['email'], unique=False)
    op.drop_table('registeration')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('registeration',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=64), nullable=True),
    sa.Column('classnum', sa.VARCHAR(length=64), nullable=True),
    sa.Column('name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('ablity', sa.TEXT(), nullable=True),
    sa.Column('desc', sa.TEXT(), nullable=True),
    sa.Column('qq', sa.VARCHAR(length=64), nullable=True),
    sa.Column('photo', sa.VARCHAR(length=32), nullable=True),
    sa.Column('wechat', sa.VARCHAR(length=64), nullable=True),
    sa.Column('telegram', sa.VARCHAR(length=64), nullable=True),
    sa.Column('personal_page', sa.TEXT(), nullable=True),
    sa.Column('phone', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index(op.f('ix_registration_email'), table_name='registration')
    op.drop_table('registration')
    ### end Alembic commands ###